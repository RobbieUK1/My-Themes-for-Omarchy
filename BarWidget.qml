import QtQuick
import Quickshell.Io
import qs.Commons as Commons
import qs.Ui as Ui

Ui.BarWidget {
  id: root
  moduleName: "io.github.robbieuk1.my-themes"
  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  Commons.Translations {
    id: strings
    directory: Qt.resolvedUrl("i18n")
  }

  // Run the bundled utility directly; no shell, installation step or download.
  Process {
    id: picker
    command: ["python3", decodeURIComponent(Qt.resolvedUrl("my-themes").toString().replace(/^file:\/\//, ""))]
  }

  Ui.WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: strings.t("button.label")
    tooltipText: strings.t("button.tooltip")
    onPressed: function(buttonCode) {
      if (picker.running) return
      if (buttonCode !== Qt.LeftButton && buttonCode !== Qt.RightButton) return
      var argv = ["python3", decodeURIComponent(Qt.resolvedUrl("my-themes").toString().replace(/^file:\/\//, ""))]
      if (buttonCode === Qt.RightButton) argv.push("--previews")
      picker.command = argv
      picker.running = true
    }
  }
}
