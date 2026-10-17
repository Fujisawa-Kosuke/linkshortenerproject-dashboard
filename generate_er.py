import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")
fig.patch.set_facecolor("#1e1e2e")
ax.set_facecolor("#1e1e2e")

table_name = "links"
columns = [
    ("id",           "INTEGER",      "PK  NOT NULL  AUTO-INCREMENT"),
    ("user_id",      "TEXT",         "NOT NULL"),
    ("original_url", "TEXT",         "NOT NULL"),
    ("short_code",   "VARCHAR(20)",  "NOT NULL  UNIQUE"),
    ("created_at",   "TIMESTAMPTZ",  "NOT NULL  DEFAULT now()"),
    ("updated_at",   "TIMESTAMPTZ",  "NOT NULL  DEFAULT now()"),
]

tbl_x = 1.2
header_y = 7.0
row_h = 0.72
tbl_w = 7.6
header_h = 0.7
col_x_name  = tbl_x + 0.18
col_x_type  = tbl_x + 2.5
col_x_const = tbl_x + 4.5

# Header
header = FancyBboxPatch((tbl_x, header_y), tbl_w, header_h,
                        boxstyle="round,pad=0.05", linewidth=1.5,
                        edgecolor="#7c6af7", facecolor="#4c3fd6")
ax.add_patch(header)
ax.text(tbl_x + tbl_w / 2, header_y + header_h / 2,
        table_name, ha="center", va="center",
        fontsize=15, fontweight="bold", color="white",
        fontfamily="monospace")

# Column rows
for i, (col, typ, constraint) in enumerate(columns):
    row_y = header_y - (i + 1) * row_h
    bg_color = "#2a2a3e" if i % 2 == 0 else "#242436"
    row = FancyBboxPatch((tbl_x, row_y), tbl_w, row_h - 0.04,
                         boxstyle="round,pad=0.02", linewidth=0.8,
                         edgecolor="#7c6af7", facecolor=bg_color)
    ax.add_patch(row)

    is_pk = "PK" in constraint
    name_color = "#f9d849" if is_pk else "#cdd6f4"
    ax.text(col_x_name, row_y + row_h / 2, col,
            ha="left", va="center", fontsize=10,
            fontweight="bold" if is_pk else "normal",
            color=name_color, fontfamily="monospace")

    ax.text(col_x_type, row_y + row_h / 2, typ,
            ha="left", va="center", fontsize=9,
            color="#89b4fa", fontfamily="monospace")

    tags = [t.strip() for t in constraint.split("  ") if t.strip()]
    tag_x = col_x_const
    TAG_COLORS = {
        "PK": "#f38ba8",
        "NOT NULL": "#a6e3a1",
        "UNIQUE": "#fab387",
        "AUTO-INCREMENT": "#cba6f7",
        "DEFAULT now()": "#74c7ec",
    }
    for tag in tags:
        tc = TAG_COLORS.get(tag, "#585b70")
        w = len(tag) * 0.105 + 0.1
        pill = FancyBboxPatch((tag_x - 0.05, row_y + 0.18), w, 0.34,
                              boxstyle="round,pad=0.04", linewidth=0,
                              facecolor=tc + "40", edgecolor=tc)
        ax.add_patch(pill)
        ax.text(tag_x + w / 2 - 0.05, row_y + row_h / 2, tag,
                ha="center", va="center", fontsize=7.5, color=tc,
                fontfamily="monospace")
        tag_x += w + 0.18

    ax.plot([col_x_type - 0.15, col_x_type - 0.15],
            [row_y + 0.08, row_y + row_h - 0.12],
            color="#7c6af7", linewidth=0.6, alpha=0.5)
    ax.plot([col_x_const - 0.15, col_x_const - 0.15],
            [row_y + 0.08, row_y + row_h - 0.12],
            color="#7c6af7", linewidth=0.6, alpha=0.5)

# Outer border
outer = FancyBboxPatch((tbl_x, header_y - len(columns) * row_h),
                       tbl_w, header_h + len(columns) * row_h,
                       boxstyle="round,pad=0.05", linewidth=2,
                       edgecolor="#7c6af7", facecolor="none")
ax.add_patch(outer)

ax.text(5, 0.35, "Generated from db/schema.ts  \u2022  Drizzle ORM  \u2022  PostgreSQL",
        ha="center", va="center", fontsize=8.5, color="#585b70",
        fontfamily="monospace")

out_path = "/Users/tom/webprojects/linkshortenerproject/er-diagram.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print(f"Saved: {out_path}")
