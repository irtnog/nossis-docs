selector_to_html = {"a[href=\"#credits\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Credits<a class=\"headerlink\" href=\"#credits\" title=\"Link to this heading\">#</a></h1><h2><a class=\"reference external\" href=\"https://github.com/iconoir-icons/iconoir/\">Iconoir</a><a class=\"headerlink\" href=\"#iconoir\" title=\"Link to this heading\">#</a></h2><p>The above files are part of Iconoir, an open source icons library with\n1600+ icons, supporting React, React Native, Flutter, Vue, Figma, and\nFramer, and are used under the terms of the\n<a class=\"reference external\" href=\"https://github.com/iconoir-icons/iconoir/blob/v7.10.0/LICENSE\">MIT License</a>,\nreproduced here in full:</p>", "a[href=\"#iconoir\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://github.com/iconoir-icons/iconoir/\">Iconoir</a><a class=\"headerlink\" href=\"#iconoir\" title=\"Link to this heading\">#</a></h2><p>The above files are part of Iconoir, an open source icons library with\n1600+ icons, supporting React, React Native, Flutter, Vue, Figma, and\nFramer, and are used under the terms of the\n<a class=\"reference external\" href=\"https://github.com/iconoir-icons/iconoir/blob/v7.10.0/LICENSE\">MIT License</a>,\nreproduced here in full:</p>"}
skip_classes = ["headerlink", "sd-stretched-link"]

window.onload = function () {
    for (const [select, tip_html] of Object.entries(selector_to_html)) {
        const links = document.querySelectorAll(` ${select}`);
        for (const link of links) {
            if (skip_classes.some(c => link.classList.contains(c))) {
                continue;
            }

            tippy(link, {
                content: tip_html,
                allowHTML: true,
                arrow: true,
                placement: 'auto-start', maxWidth: 500, interactive: false,

            });
        };
    };
    console.log("tippy tips loaded!");
};
