from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ecg import ECG

from matplotlib import pyplot as plt


class Plot:
    @staticmethod
    def show_text(text: str):
        """Display patient information in a separate figure."""
        fig_info = plt.figure(figsize=(6, 4))
        fig_info.suptitle("Patient Information")
        plt.axis("off")
        plt.text(0.01, 0.9, text, fontsize=10, verticalalignment='top',
                 wrap=True)

    @staticmethod
    def plot_lines(lines: List['ECG.Line'], title: str = "ECG Lines",
                   selected_label: Optional[str] = None):
        """Plot one or more ECG lines."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Ajout de l'axe des ordonnées
        ax.axhline(y=0, color='black', linewidth=1, linestyle='--')

        plotted_lines = Plot._add_lines_to_plot(lines, ax, selected_label)

        ax.set_title(title)
        ax.set_xlabel("Time (samples)")
        ax.set_ylabel("Amplitude")
        legend = ax.legend()

        Plot._connect_legend_click(fig, legend, plotted_lines)
        Plot._connect_keyboard_event(fig, legend, plotted_lines)

    @staticmethod
    def _add_lines_to_plot(lines: List['ECG.Line'], ax,
                           selected_label: Optional[str]):
        """Add lines to the plot and return the list of plotted line objects."""
        plotted_lines = []
        for line in lines:
            if selected_label and line.label != selected_label:
                continue
            plot_line, = ax.plot(line.points, label=line.label)
            plotted_lines.append(plot_line)
        return plotted_lines

    @staticmethod
    def _connect_legend_click(fig, legend, plotted_lines):
        """Add interactivity to toggle visibility of lines via legend clicks."""

        def on_legend_click(event):
            for l_ligne, orig_line in zip(legend.get_lines(), plotted_lines):
                if event.artist == l_ligne:
                    visible = not orig_line.get_visible()
                    orig_line.set_visible(visible)
                    l_ligne.set_alpha(1.0 if visible else 0.2)
                    fig.canvas.draw()

        fig.canvas.mpl_connect("pick_event", on_legend_click)
        for leg_line in legend.get_lines():
            leg_line.set_picker(5)

    @staticmethod
    def _connect_keyboard_event(fig, legend, plotted_lines):
        """Connect the keyboard event listener to handle specific keypress actions."""

        def on_key_press(event):
            if event.key.lower() == 'h':  # Check if the 'H' key was pressed
                for legline, origline in zip(legend.get_lines(), plotted_lines):
                    origline.set_visible(False)  # Hide the line in the plot
                    legline.set_alpha(
                        0.2)  # Make the legend entry semi-transparent
                fig.canvas.draw()

        fig.canvas.mpl_connect("key_press_event", on_key_press)

    @staticmethod
    def show():
        plt.show()
