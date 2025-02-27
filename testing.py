import streamlit as st
import requests
import json

# Streamlit UI
st.set_page_config(layout="wide")
st.title("API Testing Tool for Image URLs")

# Sidebar to store and select previously run images
st.sidebar.title("Previous Runs")
if "history" not in st.session_state:
    st.session_state.history = {}

# User inputs API URL and Image URL
api_url = st.text_input("Enter API URL:")
image_url = st.text_input("Enter Image URL:")

if st.button("Run API on Image"):
    if api_url and image_url:
        try:
            # Sending request to API with the image URL as form-data
            files = {"image_file": (image_url, requests.get(image_url).content, "image/jpeg")}
            data = {"correct": "true"}  # Sending "correct" as true

            response = requests.post(api_url, files=files, data=data)

            # Debugging: Print raw response
            st.write("Raw Response:", response.text)

            if response.status_code in [200, 201]:  # Accept both 200 and 201
                json_response = response.json()
                st.session_state.history[image_url] = json_response

                # Store the JSON response in session state for editing
                if "edited_json" not in st.session_state:
                    st.session_state.edited_json = json.dumps(json_response, indent=2)

                # Layout the output properly
                col1, col2, col3 = st.columns([1, 2, 2])

                with col1:
                    st.image(image_url, caption="Processed Image", use_column_width=True)

                with col2:
                    st.subheader("JSON Response")
                    st.json(json_response)

                with col3:
                    st.subheader("Edit JSON Response")
                    # Use session state to preserve edited JSON across refreshes
                    edited_json = st.text_area("Edit here", value=st.session_state.edited_json, height=400, key="edit_text")

                    # Update session state with the edited JSON
                    st.session_state.edited_json = edited_json

                    # Download button for edited JSON
                    st.download_button(
                        label="Download Edited JSON",
                        data=edited_json.encode('utf-8'),
                        file_name="edited_response.json",
                        mime="application/json"
                    )
            else:
                st.error(f"Failed to fetch API response. Status Code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both API URL and Image URL.")

# Sidebar toggle for viewing previous results
selected_image = st.sidebar.selectbox("Select an image to view response:", list(st.session_state.history.keys()))
if selected_image and selected_image != image_url:
    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        st.image(selected_image, caption="Selected Image", use_column_width=True)

    with col2:
        st.subheader("JSON Response")
        st.json(st.session_state.history[selected_image])

    with col3:
        st.subheader("Edit JSON Response")
        # Use session state to preserve edited JSON across refreshes
        edited_json = st.text_area("Edit here", value=json.dumps(st.session_state.history[selected_image], indent=2), height=400, key="edit_text_history")

        # Update session state with the edited JSON
        st.session_state.edited_json = edited_json

        # Download button for edited JSON
        st.download_button(
            label="Download Edited JSON",
            data=edited_json.encode('utf-8'),
            file_name="edited_response.json",
            mime="application/json"
        )
