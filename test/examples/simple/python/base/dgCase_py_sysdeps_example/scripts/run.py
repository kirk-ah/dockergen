from PIL import Image, ImageDraw
from lxml import etree
import psycopg2

def demo_image():
    img = Image.new("RGB", (200, 100), color="blue")
    draw = ImageDraw.Draw(img)
    draw.text((10, 40), "Disc Golf Rocks!", fill="white")
    img.save("demo.png")
    print("✅ Image saved as demo.png")

def demo_xml():
    root = etree.Element("root")
    child = etree.SubElement(root, "message")
    child.text = "Hello from lxml"
    tree = etree.ElementTree(root)
    tree.write("demo.xml", pretty_print=True)
    print("✅ XML saved as demo.xml")

def demo_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("✅ Postgres version:", cur.fetchone())
        conn.close()
    except Exception as e:
        print("⚠️ Could not connect to Postgres:", e)

if __name__ == "__main__":
    demo_image()
    demo_xml()
    demo_db()