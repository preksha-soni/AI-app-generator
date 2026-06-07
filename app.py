import google.generativeai as genai
import json
import streamlit as st
import os

# ---- CONFIG ----
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-flash"  # Free tier model

# ---- HELPER: Call Gemini ----
def call_gemini(system_prompt, user_prompt):
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt
    )
    response = model.generate_content(user_prompt)
    return response.text

# ---- HELPER: Extract and validate JSON ----
def extract_json(text):
    try:
        return json.loads(text)
    except:
        import re
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        return None

# ---- REPAIR: Fix broken JSON ----
def repair_json(broken_json_text, original_prompt):
    repair_prompt = f"""
The following JSON is broken or incomplete. Fix it and return ONLY valid JSON, nothing else.
No explanation, no markdown, no code blocks. Just raw JSON.

Original user request: {original_prompt}

Broken JSON:
{broken_json_text}
"""
    repaired = call_gemini(
        "You are a JSON repair expert. Return only valid raw JSON, nothing else.",
        repair_prompt
    )
    return extract_json(repaired)

# =======================================
# STAGE 1: Intent Extraction
# =======================================
def stage1_extract_intent(user_prompt):
    system = """You are an expert software architect.
Extract the user's intent into structured JSON.
Return ONLY raw JSON, no markdown, no explanation.
Format:
{
  "app_name": "string",
  "app_type": "string",
  "core_features": ["list of features"],
  "user_roles": ["list of roles"],
  "auth_required": true/false,
  "payment_required": true/false,
  "key_entities": ["main data entities"]
}"""
    result = call_gemini(system, f"Extract intent from: {user_prompt}")
    parsed = extract_json(result)
    if not parsed:
        parsed = repair_json(result, user_prompt)
    return parsed

# =======================================
# STAGE 2: System Architecture
# =======================================
def stage2_system_architecture(intent, user_prompt):
    system = """You are a senior system architect.
Design the app architecture based on the intent.
Return ONLY raw JSON, no markdown, no explanation.
Format:
{
  "pages": [{"name": "string", "route": "string", "access": "role or public"}],
  "entities": [{"name": "string", "description": "string"}],
  "auth_flows": ["login", "register", etc],
  "integrations": ["payments", "email", etc]
}"""
    result = call_gemini(system, f"Design architecture for:\nIntent: {json.dumps(intent)}\nOriginal: {user_prompt}")
    parsed = extract_json(result)
    if not parsed:
        parsed = repair_json(result, user_prompt)
    return parsed

# =======================================
# STAGE 3: Schema Generation
# =======================================
def stage3_generate_schemas(intent, architecture, user_prompt):
    system = """You are a full-stack schema expert.
Generate complete schemas based on intent and architecture.
Return ONLY raw JSON, no markdown, no explanation.
Format:
{
  "ui_schema": {
    "pages": [{"name": "string", "components": ["list"], "layout": "string"}]
  },
  "api_schema": {
    "endpoints": [{"path": "string", "method": "GET/POST/PUT/DELETE", "auth_required": true/false, "request_body": {}, "response": {}}]
  },
  "db_schema": {
    "tables": [{"name": "string", "fields": [{"name": "string", "type": "string", "required": true/false}], "relations": []}]
  },
  "auth_schema": {
    "roles": ["list"],
    "permissions": {"role": ["allowed actions"]}
  }
}"""
    result = call_gemini(system, f"Generate schemas for:\nIntent: {json.dumps(intent)}\nArchitecture: {json.dumps(architecture)}")
    parsed = extract_json(result)
    if not parsed:
        parsed = repair_json(result, user_prompt)
    return parsed

# =======================================
# STAGE 4: Validation + Repair
# =======================================
def stage4_validate_and_repair(schemas, intent, architecture):
    errors = []
    required_keys = ["ui_schema", "api_schema", "db_schema", "auth_schema"]
    for key in required_keys:
        if key not in schemas:
            errors.append(f"Missing key: {key}")

    if errors:
        fix_prompt = f"""
Fix these issues in the schema and return complete valid JSON only:
Issues: {errors}
Current schemas: {json.dumps(schemas)}
Intent: {json.dumps(intent)}
Architecture: {json.dumps(architecture)}
"""
        fixed = call_gemini(
            "You are a schema validator. Fix all issues and return only raw valid JSON.",
            fix_prompt
        )
        schemas = extract_json(fixed) or schemas
        errors = []

    consistency_prompt = f"""
Check and fix cross-layer consistency in these schemas:
- API fields must match DB schema fields
- UI fields must map to API endpoints
- Auth roles must be consistent across all layers
Return the fixed complete schemas as raw JSON only.
Schemas: {json.dumps(schemas)}
"""
    consistent = call_gemini(
        "You are a consistency checker. Return only raw valid JSON with all inconsistencies fixed.",
        consistency_prompt
    )
    final = extract_json(consistent) or schemas
    return final, errors

# =======================================
# FULL PIPELINE
# =======================================
def run_pipeline(user_prompt):
    results = {}
    intent = stage1_extract_intent(user_prompt)
    results["stage1_intent"] = intent
    architecture = stage2_system_architecture(intent, user_prompt)
    results["stage2_architecture"] = architecture
    schemas = stage3_generate_schemas(intent, architecture, user_prompt)
    results["stage3_schemas"] = schemas
    final_schemas, errors = stage4_validate_and_repair(schemas, intent, architecture)
    results["stage4_final"] = final_schemas
    results["validation_errors_found_and_fixed"] = errors
    return results

# =======================================
# STREAMLIT UI
# =======================================
def main():
    st.set_page_config(page_title="AI App Generator", page_icon="🤖", layout="wide")
    st.title("🤖 AI App Generator")
    st.markdown("**Natural Language → Complete App Schema**")
    st.markdown("---")

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    st.markdown("### 💡 Example Prompts")
    examples = [
        "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments",
        "Create a todo app with user authentication and team collaboration",
        "Build an e-commerce store with product listings, cart, checkout and admin panel"
    ]
    for ex in examples:
        if st.button(f"📌 {ex[:60]}..."):
            st.session_state.prompt = ex
            st.rerun()

    user_prompt = st.text_area(
        "Describe your app:",
        value=st.session_state.prompt,
        height=100,
        placeholder="e.g. Build a CRM with login, contacts, dashboard..."
    )

    if st.button("🚀 Generate App Schema", type="primary"):
        if not user_prompt.strip():
            st.error("Please enter a prompt!")
        else:
            with st.spinner("Running 4-stage pipeline..."):
                progress = st.progress(0)
                status = st.empty()
                try:
                    status.text("Stage 1: Extracting Intent...")
                    progress.progress(10)
                    intent = stage1_extract_intent(user_prompt)
                    progress.progress(25)

                    status.text("Stage 2: Designing Architecture...")
                    architecture = stage2_system_architecture(intent, user_prompt)
                    progress.progress(50)

                    status.text("Stage 3: Generating Schemas...")
                    schemas = stage3_generate_schemas(intent, architecture, user_prompt)
                    progress.progress(75)

                    status.text("Stage 4: Validating & Repairing...")
                    final_schemas, errors = stage4_validate_and_repair(schemas, intent, architecture)
                    progress.progress(100)
                    status.text("✅ Done!")

                    results = {
                        "stage1_intent": intent,
                        "stage2_architecture": architecture,
                        "stage3_schemas": schemas,
                        "stage4_final": final_schemas,
                        "validation_errors_fixed": errors
                    }

                    st.success("✅ Pipeline Complete!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🎯 Stage 1: Intent")
                        st.json(intent)
                        st.markdown("### 🏗️ Stage 2: Architecture")
                        st.json(architecture)
                    with col2:
                        st.markdown("### 📋 Stage 3: Schemas")
                        st.json(schemas)
                        st.markdown("### ✅ Stage 4: Final Validated Schema")
                        st.json(final_schemas)

                    if errors:
                        st.warning(f"⚠️ Found and fixed {len(errors)} issues: {errors}")
                    else:
                        st.success("✅ No validation errors found!")

                    st.download_button(
                        "⬇️ Download Full Schema JSON",
                        data=json.dumps(results, indent=2),
                        file_name="app_schema.json",
                        mime="application/json"
                    )

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Try again or simplify your prompt")

if __name__ == "__main__":
    main()
