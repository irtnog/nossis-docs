selector_to_html = {"a[href=\"#module-nossis_docs.test\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test\" title=\"nossis_docs.test\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test\" title=\"Link to this heading\">#</a></h1><p>Bundle functional and integration tests in the distribution, which\nfacilitates the operational qualification of production deployments.</p>", "a[href=\"#submodules\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Submodules<a class=\"headerlink\" href=\"#submodules\" title=\"Link to this heading\">#</a></h2>", "a[href=\"nossis_docs.test.test_pipeline.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"nossis_docs.test.test_pipeline\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test.test_pipeline</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"Link to this heading\">#</a></h1><h2>Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">#</a></h2><h3>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">#</a></h3>", "a[href=\"nossis_docs.test.conftest.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test.conftest\" title=\"nossis_docs.test.conftest\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test.conftest</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test.conftest\" title=\"Link to this heading\">#</a></h1><p>Configure test fixtures (mocks).</p>"}
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
