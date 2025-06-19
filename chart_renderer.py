# chart_renderer.py
# Visualization module for astrological charts

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.table import Table
from astro_constants import AstroConstants
from astro_utils import AstroUtils
from astro_calculator import AstroCalculator

class ChartRenderer:
    @staticmethod
    def create_chart(chart_data, name, date_str, output_filename="mapa_astral.pdf"):
        """
        Create and save astrological chart.
        
        Args:
            chart_data: Dictionary with houses, planets positions
            name: String, person's name
            date_str: String, formatted date
            output_filename: String, output file path
        """
        positions = chart_data["positions"]
        houses = chart_data["houses"]
        aspects = AstroCalculator.calculate_aspects(positions)
        
        # Create figure
        fig = plt.figure(figsize=(14, 12))
        
        # Create wheel chart
        ChartRenderer._create_wheel_chart(fig, positions, houses, name, date_str)
        
        # Create aspects table
        ChartRenderer._create_aspects_table(fig, positions)
        
        # Create positions table
        ChartRenderer._create_positions_table(fig, positions)
        
        plt.tight_layout()
        fig.savefig(output_filename)
        return fig
    
    @staticmethod
    def _create_wheel_chart(fig, positions, houses, name, date_str):
        """Create the wheel chart."""
        ax = fig.add_subplot(121, projection='polar')
        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_yticklabels([])
        ax.set_xticks([])
        
        # Add title and date
        fig.text(0.03, 0.96, name, fontsize=16, fontweight='bold', ha='left')
        fig.text(0.03, 0.92, date_str, fontsize=14, ha='left')
        
        # Draw zodiac signs
        for i, sign in enumerate(AstroConstants.SIGNS):
            ang = 360 - (i * 30 + 15) + 90
            theta = np.radians(ang)
            x, y = np.cos(theta) * 0.84, np.sin(theta) * 0.84
            circle = Circle((x, y), 0.045, transform=ax.transData._b, facecolor='#fff8cc', edgecolor='none')
            ax.add_patch(circle)
            ax.text(theta, 0.84, sign, fontsize=22, fontweight='bold', ha='center', va='center')
        
        # Draw house lines
        for i in range(12):
            degree = houses[i]
            theta = np.radians(360 - degree + 90)
            ax.plot([theta, theta], [0, 1], color='black', linewidth=1.8)
            ax.text(theta, 1.12, AstroUtils.format_degrees(degree), fontsize=8, ha='center', va='center')
        
        # Draw planets
        sectors = {}
        for planet_name, degree in sorted(positions.items(), key=lambda x: x[1]):
            sector = int(degree)
            offset = sectors.get(sector, 0)
            theta = np.radians(360 - degree + 90)
            ax.text(theta, 1.05 - offset * 0.07, planet_name, fontsize=15, fontweight='bold', ha='center')
            sectors[sector] = offset + 1
        
        # Draw aspect lines
        keys = list(positions.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a1, a2 = positions[keys[i]], positions[keys[j]]
                diff = abs(a1 - a2) % 360
                for degree, cfg in AstroConstants.ASPECTS.items():
                    if abs(diff - degree) <= cfg['tol']:
                        t1 = np.radians(360 - a1 + 90)
                        t2 = np.radians(360 - a2 + 90)
                        ax.plot([t1, t2], [1, 1], color=cfg['cor'], linestyle=cfg['estilo'], alpha=0.6, linewidth=1)
                        break
    
    @staticmethod
    def _create_aspects_table(fig, positions):
        """Create aspects table."""
        ax2 = fig.add_subplot(222)
        ax2.set_axis_off()
        table = Table(ax2, bbox=[0, 0, 1, 1])
        names = list(positions.keys())
        n = len(names)
        cw = 1.0 / (n + 1)
        ch = 1.0 / (n + 1)
        
        for i in range(n + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    table.add_cell(i, j, cw, ch, text="", loc='center')
                elif i == 0:
                    table.add_cell(i, j, cw, ch, text=names[j - 1], loc='center', facecolor='#f0f0f0')
                elif j == 0:
                    table.add_cell(i, j, cw, ch, text=names[i - 1], loc='center', facecolor='#f0f0f0')
                elif j < i:
                    ang = abs(positions[names[i - 1]] - positions[names[j - 1]]) % 360
                    symbol = ""
                    color = "black"
                    for degree, cfg in AstroConstants.ASPECTS.items():
                        if abs(ang - degree) <= cfg['tol']:
                            symbol = cfg['simbolo']
                            color = cfg['cor']
                            break
                    cell = table.add_cell(i, j, cw, ch, text=symbol, loc='center', facecolor='white')
                    cell.get_text().set_color(color)
                else:
                    table.add_cell(i, j, cw, ch, text="", loc='center', facecolor='lightgrey')
        
        ax2.add_table(table)
    
    @staticmethod
    def _create_positions_table(fig, positions):
        """Create positions table."""
        ax3 = fig.add_axes([0.51, 0.05, 0.45, 0.35])
        ax3.set_axis_off()
        pos_table = Table(ax3, bbox=[0, 0, 1, 1])
        row_height = 1.0 / (len(positions) + 1)
        pos_table.add_cell(0, 0, 0.5, row_height, text="Planeta", loc='center', facecolor='#f0f0f0')
        pos_table.add_cell(0, 1, 0.5, row_height, text="Posição", loc='center', facecolor='#f0f0f0')
        
        for i, planet_name in enumerate(positions.keys()):
            degree = positions[planet_name]
            sign = AstroConstants.SIGNS[int(degree // 30)]
            deg = int(degree % 30)
            mins = int((degree % 1) * 60)
            degree_fmt = f"{deg}° {mins:02d}′"
            pos_table.add_cell(i + 1, 0, 0.5, row_height, text=planet_name, loc='center')
            pos_table.add_cell(i + 1, 1, 0.5, row_height, text=f"{degree_fmt} {sign}", loc='center')
        
        ax3.add_table(pos_table)