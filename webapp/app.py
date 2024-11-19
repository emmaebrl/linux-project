import streamlit as st


def main():
    # Title of the app
    st.title("Simple Testing Interface")

    # Section for text input
    st.subheader("Text Input Test")
    user_text = st.text_input("Enter some text", value="Sample text")
    if st.button("Submit Text"):
        st.write(f"You entered: {user_text}")

    # Section for number input
    st.subheader("Number Input Test")
    user_number = st.number_input(
        "Enter a number", min_value=0, max_value=100, value=50
    )
    if st.button("Submit Number"):
        st.write(f"You entered: {user_number}")

    # Section for selecting options
    st.subheader("Options Test")
    options = ["Option 1", "Option 2", "Option 3"]
    selected_option = st.selectbox("Choose an option", options)
    st.write(f"You selected: {selected_option}")

    # Section for slider input
    st.subheader("Slider Test")
    slider_value = st.slider("Choose a value", min_value=0, max_value=100, value=25)
    st.write(f"Slider value: {slider_value}")

    # Section for checkbox
    st.subheader("Checkbox Test")
    agree = st.checkbox("I agree to the terms and conditions")
    if agree:
        st.write("Thank you for agreeing!")
    else:
        st.write("Please agree to the terms and conditions to proceed.")

    # Section for displaying results
    st.subheader("Results")
    if st.button("Show Results"):
        st.write("Text:", user_text)
        st.write("Number:", user_number)
        st.write("Selected Option:", selected_option)
        st.write("Slider Value:", slider_value)
        st.write("Agreement:", "Agreed" if agree else "Not Agreed")


if __name__ == "__main__":
    main()
