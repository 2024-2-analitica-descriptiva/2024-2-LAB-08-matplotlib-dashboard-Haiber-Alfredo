# pylint: disable=line-too-long
"""
Escriba el código que ejecute la acción solicitada.
"""
import matplotlib.pyplot as plt
import pandas as pd
import os

def pregunta_01():
    """
    El archivo `files/input/shipping-data.csv` contiene información sobre los envíos
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `files/input`.

    * Todos los archivos deben ser creados en la carpeta `files/docs`.

    * Su código debe crear la carpeta `files/docs` si no existe.
    """
    input_file = 'files/input/shipping-data.csv'
    output_directory = 'docs'

    # Crear el directorio de salida si no existe
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Cargar los datos
    df = load_data(input_file)

    # Crear visualización
    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_mode_of_shipment(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)
    create_dashboard_html("docs/index.html")



def load_data(input_file):
    """Carga los datos desde un archivo CSV."""
    return pd.read_csv(input_file)


def create_visual_for_shipping_per_warehouse(df):
    """Crea un gráfico de envíos por almacén."""
    df = df.copy()
    plt.figure()
    counts = df.Warehouse_block.value_counts()
    counts.plot.bar(
        title='Shipping per Warehouse',
        xlabel='Warehouse block',
        ylabel='Record Count',
        color='tab:blue',
        fontsize=8,
    )
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.savefig('docs/shipping_per_warehouse.png')
    plt.close()

# Visual for Mode of Shipment
def create_visual_for_mode_of_shipment(df):
    df = df.copy()
    plt.figure()
    counts = df.Mode_of_Shipment.value_counts()
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )
    plt.savefig("docs/mode_of_shipment.png")
    plt.close()

# Visual for Average Customer Rating
def create_visual_for_average_customer_rating(df):
    df = df.copy()
    plt.figure()
    df = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df.columns = df.columns.droplevel()
    df = df[["mean", "min", "max"]]
    plt.barh(
        y=df.index.values,
        width=df["max"].values - 1,
        left=df["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df["mean"].values
    ]

    plt.barh(
        y=df.index.values,
        width=df["mean"].values - 1,
        left=df["min"].values,
        color=colors,
        height=0.5,
        alpha=1.0,
    )
    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/average_customer_rating.png")
    plt.close()

# Visual for Weight Distribution
def create_visual_for_weight_distribution(df):
    df = df.copy()
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/weight_distribution.png")

def create_dashboard_html(output_file="docs/index.html"):
    """
    Genera un archivo HTML para mostrar el dashboard con los gráficos generados.
    
    Parámetros:
    - output_file: Nombre o ruta del archivo HTML a generar.
    """
    html_content = """<!DOCTYPE html>
<html>
<body>
    <h1>Shipping Dashboard Example</h1>
    <div style="width:45%;float:left">
        <img src="docs/shipping_per_warehouse.png" alt="Fig 1">
        <img src="docs/mode_of_shipment.png" alt="Fig 2">
    </div>
    <div style="width:45%;float:left">
        <img src="docs/average_customer_rating.png" alt="Fig 3">
        <img src="docs/weight_distribution.png" alt="Fig 4">
    </div>
</body>
</html>"""

    # Crear el archivo HTML
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"Dashboard HTML generado en {output_file}")

if __name__ == "__main__":
    pregunta_01()
