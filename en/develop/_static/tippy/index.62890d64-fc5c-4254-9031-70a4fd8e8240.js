selector_to_html = {"a[href=\"#sd-hide-title-true\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">sd_hide_title: True<a class=\"headerlink\" href=\"#sd-hide-title-true\" title=\"Link to this heading\">#</a></h1>", "a[href=\"#welcome\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Welcome<a class=\"headerlink\" href=\"#welcome\" title=\"Link to this heading\">#</a></h1>"}
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
