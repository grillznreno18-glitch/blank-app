import streamlit as st
import pandas as pd
import re

st.title("S&S Activewear SKU Image Linker")
st.write("Upload your Excel file to automatically append CDN image URLs.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Ask the user which column holds the SKUs
    sku_col = st.selectbox("Select the SKU column:", df.columns)

    if st.button("Process Spreadsheet"):
        base_cdn = "https://ssactivewear.com"

        def clean_sku(sku):
            # Extract leading numbers/characters representing Style ID
            match = re.match(r"^([a-zA-Z0-9]+)", str(sku).strip())
            return f"{base_cdn}{match.group(1)}_fl.jpg" if match else ""

        df['S&S_Image_URL'] = df[sku_col].apply(clean_sku)

        st.success("Processing complete!")
        st.dataframe(df.head()) # Preview the data

        # Convert dataframe back to excel for download
        @st.cache_data
        def convert_df(df_to_save):
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_to_save.to_excel(writer, index=False)
            return output.getvalue()

        xlsx_data = convert_df(df)
        st.download_button("📥 Download Processed Excel File", data=xlsx_data, file_name="ss_mapped_images.xlsx")
