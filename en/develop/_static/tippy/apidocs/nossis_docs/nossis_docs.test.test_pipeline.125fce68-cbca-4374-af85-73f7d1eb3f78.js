selector_to_html = {"a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">#</a></h2><h3>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">#</a></h3>", "a[href=\"#module-nossis_docs.test.test_pipeline\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference internal\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"nossis_docs.test.test_pipeline\"><code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">nossis_docs.test.test_pipeline</span></code></a><a class=\"headerlink\" href=\"#module-nossis_docs.test.test_pipeline\" title=\"Link to this heading\">#</a></h1><h2>Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">#</a></h2><h3>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">#</a></h3>", "a[href=\"#api\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">API<a class=\"headerlink\" href=\"#api\" title=\"Link to this heading\">#</a></h3>", "a[href=\"#nossis_docs.test.test_pipeline.test_invalidate_distribution\"]": "<dt class=\"sig sig-object py\" id=\"nossis_docs.test.test_pipeline.test_invalidate_distribution\">\n<span class=\"sig-prename descclassname\"><span class=\"pre\">nossis_docs.test.test_pipeline.</span></span><span class=\"sig-name descname\"><span class=\"pre\">test_invalidate_distribution</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">distribution</span></span><span class=\"p\"><span class=\"pre\">:</span></span><span class=\"w\"> </span><span class=\"n\"><span class=\"pre\">mypy_boto3_cloudfront.type_defs.CreateDistributionResultTypeDef</span></span></em><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">None</span></span></span><a class=\"reference internal\" href=\"../../_modules/nossis_docs/test/test_pipeline.html#test_invalidate_distribution\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Simulate a CodePipeline deploy stage signaling Lambda to\ninvalidate paths in a CloudFront distribution.</p></dd>", "a[href=\"#functions\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">#</a></h3>"}
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
