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
        """Plot one or more ECG lines with peaks."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Ajout de l'axe des ordonnées
        ax.axhline(y=0, color='black', linewidth=1, linestyle='--')

        plotted_lines, peak_points = Plot._add_lines_and_peaks_to_plot(
            lines, ax, selected_label
        )

        ax.set_title(title)
        ax.set_xlabel("Time (samples)")
        ax.set_ylabel("Amplitude")
        legend = ax.legend()

        Plot._connect_legend_click(fig, legend, plotted_lines, peak_points)
        Plot._connect_keyboard_event(fig, legend, plotted_lines, peak_points)

    @staticmethod
    def _add_lines_and_peaks_to_plot(lines: List['ECG.Line'], ax,
                                     selected_label: Optional[str]):
        """Add lines and peaks to the plot."""
        plotted_lines = []
        peak_points = []

        for line in lines:
            if selected_label and line.label != selected_label:
                continue

            # Plot the line
            plot_line, = ax.plot(line.points, label=line.label)
            plotted_lines.append(plot_line)

            # Plot the peaks as scatter points
            peaks_idx = line.metadata and line.metadata.values() or []
            # flatten
            peaks_idx = [item for sublist in peaks_idx for item in sublist]
            peak_points_line = ax.scatter([i for i in peaks_idx if not i != i],
                                          [line.points[i] for i in peaks_idx if
                                           not i != i],
                                          color=plot_line.get_color())
            peak_points.append(peak_points_line)

        return plotted_lines, peak_points

    @staticmethod
    def _connect_legend_click(fig, legend, plotted_lines, peak_points):
        """Toggle visibility of lines and peaks via legend clicks."""

        def on_legend_click(event):
            for l_leg, orig_line, peak_point in zip(legend.get_lines(),
                                                    plotted_lines, peak_points):
                if event.artist == l_leg:
                    # Toggle visibility
                    visible = not orig_line.get_visible()
                    orig_line.set_visible(visible)
                    peak_point.set_visible(visible)
                    l_leg.set_alpha(1.0 if visible else 0.2)
                    fig.canvas.draw()

        fig.canvas.mpl_connect("pick_event", on_legend_click)
        for leg_line in legend.get_lines():
            leg_line.set_picker(5)

    @staticmethod
    def _connect_keyboard_event(fig, legend, plotted_lines, peak_points):
        """Hide all lines and peaks when pressing 'H'."""

        def on_key_press(event):
            if event.key.lower() == 'h':  # Check if 'H' key is pressed
                for legline, origline, peakpoint in zip(
                        legend.get_lines(), plotted_lines, peak_points):
                    origline.set_visible(False)  # Hide the line
                    peakpoint.set_visible(False)  # Hide the points
                    legline.set_alpha(0.2)  # Semi-transparent legend
                fig.canvas.draw()

        fig.canvas.mpl_connect("key_press_event", on_key_press)

    @staticmethod
    def show():
        plt.show()
