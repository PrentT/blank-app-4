import streamlit as st
import json
import difflib


# Function to load JSON from uploaded files
def load_json(file):
    try:
        return json.load(file)
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON.")
        return None

# Function to get the line-by-line diff between two JSON strings
def get_line_diff(json1, json2):
    json1_str = json.dumps(json1, indent=2).splitlines(keepends=True)
    json2_str = json.dumps(json2, indent=2).splitlines(keepends=True)
    d = difflib.unified_diff(json1_str, json2_str, lineterm='')
    return list(d)

# Streamlit app setup
st.title("JSON Files Comparison Tool")

# Upload JSON files
file1 = st.file_uploader("Upload the first JSON file", type="json")
file2 = st.file_uploader("Upload the second JSON file", type="json")

if file1 and file2:
    json1 = load_json(file1)
    json2 = load_json(file2)
    
    if json1 is not None and json2 is not None:
        # Show the JSON diff in a readable format
        st.header("Differences between JSON files:")
        line_diff = get_line_diff(json1, json2)
        
        if line_diff:
            for line in line_diff:
                # Highlight added, removed, and context lines
                if line.startswith("+") and not line.startswith("+++"):
                    st.markdown(f'<span style="color: green;">{line}</span>', unsafe_allow_html=True)
                elif line.startswith("-") and not line.startswith("---"):
                    st.markdown(f'<span style="color: red;">{line}</span>', unsafe_allow_html=True)
                else:
                    st.text(line)
        else:
            st.success("The JSON files are identical!")
    else:
        st.error("Failed to load one or both JSON files.")
