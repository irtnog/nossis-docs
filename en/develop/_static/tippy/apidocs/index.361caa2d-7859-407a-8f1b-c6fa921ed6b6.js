selector_to_html = {"a[href=\"nossis_docs/nossis_docs.test.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test\" title=\"nossis_docs.test\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test\" title=\"Link to this heading\">#</a></h1><p>Bundle functional and integration tests in the distribution, which\nfacilitates the operational qualification of production deployments.</p>", "a[href=\"nossis_docs/nossis_docs.pipeline.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.pipeline\" title=\"nossis_docs.pipeline\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.pipeline</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.pipeline\" title=\"Link to this heading\">#</a></h1><p>AWS Lambda actions for CodePipeline.</p>", "a[href=\"nossis_docs/nossis_docs.test.conftest.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test.conftest\" title=\"nossis_docs.test.conftest\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test.conftest</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test.conftest\" title=\"Link to this heading\">#</a></h1><p>Configure test fixtures (mocks).</p>", "a[href=\"#f1\"]": "<aside class=\"footnote brackets\" id=\"f1\" role=\"doc-footnote\">\n<span class=\"label\"><span class=\"fn-bracket\">[</span><a href=\"#id1\" role=\"doc-backlink\">1</a><span class=\"fn-bracket\">]</span></span>\n<p>Created with <a class=\"reference external\" href=\"https://github.com/chrisjsewell/sphinx-autodoc2\">sphinx-autodoc2</a></p>\n</aside>", "a[href=\"#api-reference\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">API Reference<a class=\"headerlink\" href=\"#api-reference\" title=\"Link to this heading\">#</a></h1><p>This page contains auto-generated API reference documentation <a class=\"footnote-reference brackets\" href=\"#f1\" id=\"id1\" role=\"doc-noteref\"><span class=\"fn-bracket\">[</span>1<span class=\"fn-bracket\">]</span></a>.</p>", "a[href=\"nossis_docs/nossis_docs.test.test_pipeline.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"nossis_docs.test.test_pipeline\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test.test_pipeline</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"Link to this heading\">#</a></h1><h2>Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">#</a></h2><h3>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">#</a></h3>", "a[href=\"nossis_docs/nossis_docs.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs\" title=\"nossis_docs\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs\" title=\"Link to this heading\">#</a></h1><p>Initialize the module and export top-level public interfaces.</p>"}
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
