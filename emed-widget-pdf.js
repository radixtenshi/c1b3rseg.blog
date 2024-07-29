
  function loadIframes() {
    if (window.__smallpdfAutoLoadIframeTimerID != null) {
      return;
    }

    function addIFrameIfNotExists(container) {
      if (container != null && container.querySelector(".smallpdf-widget-iframe") == null) {
        container.innerHTML = "";

        const iframe = document.createElement('iframe');

        iframe.setAttribute("class", "smallpdf-widget-iframe");

        const pdfUrl = container.getAttribute("data-pdf-url");
        const pdfFilename = container.getAttribute("data-pdf-filename");

        let src = "https://smallpdf.com/reader-embedded#";

        src += `url=${encodeURIComponent(pdfUrl)}`

        if (pdfFilename) {
          src += `&filename=${pdfFilename}`
        }

        iframe.setAttribute('src', src);

        iframe.setAttribute("width", "100%");
        iframe.setAttribute("height", "100%");
        iframe.setAttribute("style", "width: 100%; height: 100%; background: rgba(0,34,102,0); color: white;");
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("allow", "fullscreen");

        container.appendChild(iframe);
      }
    }

    window.__smallpdfAutoLoadIframeTimerID = window.setInterval(function () {
      const containers = document.querySelectorAll(".smallpdf-widget");
      Array.from(containers).forEach((container) => {
        addIFrameIfNotExists(container);
      });
    }, 1500);

    const containers = document.querySelectorAll(".smallpdf-widget");
    Array.from(containers).forEach((container) => {
      addIFrameIfNotExists(container);
    });
  }

  (function () {
    if (document.readyState === "complete") {
      loadIframes();
    }
    else {
      addEventListener("DOMContentLoaded", loadIframes);
      addEventListener("load", loadIframes);
    }
  })();
  
