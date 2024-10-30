# import streamlit as st

# # Display car details if a car is selected
# if "selected_car" in st.session_state:
#     car = st.session_state.selected_car
#     Name, Color, No_of_seats, Price, Type, Brand = car
#     st.title(f"Your {Brand} {Name}")

#     # Display car image on the left and details on the right
#     left, right = st.columns([1, 2])

#     with left:
#         # st.image(f"images/{Brand.lower()}_{Name.lower()}.png", caption=f"{Brand} {Name}")
#         st.image(f"Images/image.png", caption=f"{Brand} {Name}")

#     with right:
#         st.write(f"**Type:** {Type}")
#         st.write(f"**Color:** {Color}")
#         st.write(f"**Seats:** {No_of_seats}")
#         st.write(f"**Price:** Rs. {Price}")
#         if st.button("Book Car"):
#             st.success("Booking confirmed!")

# # Redirect to main page if no car is selected
# else:
#     st.warning("No car selected. Redirecting to home...")
#     # st.experimental_set_query_params(page="home")
#     st.switch_page("homepage.py")

import streamlit as st

# Display car details if a car is selected
if "selected_car" in st.session_state:
    car = st.session_state.selected_car
    Name, Color, No_of_seats, Price, Type, Brand = car
    st.title(f"Your {Brand} {Name}")

    # Display car image on the left and details on the right
    left, right = st.columns([2, 3])

    with left:
        # Increase the width of the image (adjust as necessary)
        st.image(f"Images/image.png", caption=f"{Brand} {Name}", width = 400)  # Set width to 300px

    with right:
        st.write(f"**Type:** {Type}")
        st.write(f"**Color:** {Color}")
        st.write(f"**Seats:** {No_of_seats}")
        st.write(f"**Price:** Rs. {Price}")
        if st.button("Book Car"):
            st.success("Booking confirmed!")

# Redirect to main page if no car is selected
else:
    st.warning("No car selected. Redirecting to home...")
    st.switch
