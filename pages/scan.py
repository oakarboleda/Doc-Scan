import pyinsane2
import streamlit as st


def scan_document():
    st.write("Scanning document...")
    try:
        # Initialize pyinsane2 and get scanner devices
        devices = pyinsane2.get_devices()
        if not devices:
            st.error("No scanners found.")
            return

        scanner = devices[0]
        st.write(f"Using scanner: {scanner.name}")

        # Start scanning; only one image is expected from a single scan
        scan_session = scanner.scan(multiple=False)
        st.info("Scanning, please wait...")
        images = []
        while True:
            try:
                # Retrieve the scanned image
                image = scan_session.next()
                images.append(image)
            except pyinsane2.PyInsaneException:
                break

        if images:
            scanned_image = images[0]
            st.image(scanned_image, caption="Scanned Document", use_column_width=True)
            # Optionally, save the scanned image
            image_file = "./scanned_document.png"
            scanned_image.save(image_file)
            st.success(f"Document scanned and saved as {image_file}")
        else:
            st.error("No image captured during scanning.")
    except Exception as e:
        st.error(f"Error during scanning: {e}")

if st.button("Scan Document"):
    scan_document()