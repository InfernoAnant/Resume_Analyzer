import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from collections import Counter
import io
import base64

def generate_dashboard_chart(roles):

    role_counts = Counter(roles)

    plt.figure(figsize=(8, 5))
    plt.pie(
        role_counts.values(),
        labels=role_counts.keys(),
        autopct="%1.1f%%",
        startangle=140
    )

    plt.xlabel("Roles")
    plt.ylabel("Count")
    plt.title("Role Distribution Analytics")
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    
    chart_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return chart_data