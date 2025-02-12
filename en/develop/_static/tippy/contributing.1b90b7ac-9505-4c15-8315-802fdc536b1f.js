selector_to_html = {"a[href=\"#commit-messages\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Commit Messages<a class=\"headerlink\" href=\"#commit-messages\" title=\"Link to this heading\">#</a></h2><p>This project implements\n<a class=\"reference external\" href=\"https://semver.org/spec/v2.0.0.html\">Semantic Versioning 2.0.0</a> using\n<a class=\"reference external\" href=\"https://www.conventionalcommits.org/en/v1.0.0/\">Conventional Commits 1.0.0</a>.\nPlease use English in commit messages.  The first line of the commit\nmessage should be at most 100 characters, while the rest of the commit\nmessage should be wrapped at column 70.  A commit\u2019s description should\nbe a verb phrase in the imperative present tense, with the starting\nverb in lower case and no ending punctuation.</p><p>Valid commit types are:</p>", "a[href=\"#contributing\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Contributing<a class=\"headerlink\" href=\"#contributing\" title=\"Link to this heading\">#</a></h1><p>This project combines <a class=\"reference external\" href=\"https://tdd.mooc.fi/\">test-driven development</a>,\n<a class=\"reference external\" href=\"https://www.aleksandrhovhannisyan.com/blog/atomic-git-commits/\">atomic commits</a>,\na <a class=\"reference external\" href=\"https://archive.is/VpWTs\">linear commit history</a>, and the\n<a class=\"reference external\" href=\"https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow\">Git feature branch workflow</a>.\nPlease rebase your changes on the latest HEAD of the main branch\nbefore submitting them for review as a\n<a class=\"reference external\" href=\"https://docs.github.com/en/pull-requests/collaborating-with-pull-requests\">GitHub pull request</a>.\nChanges must include updated functional and integration tests.</p>", "a[href=\"#code-style\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Code Style<a class=\"headerlink\" href=\"#code-style\" title=\"Link to this heading\">#</a></h2><p>This project follows these code styles:</p>", "a[href=\"#development-environment\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Development Environment<a class=\"headerlink\" href=\"#development-environment\" title=\"Link to this heading\">#</a></h2><p>This project requires Python 3.11 and OpenTofu 1.8 (or newer).  To set\nup your development environment on Linux or macOS, run these\n<a class=\"reference external\" href=\"https://www.gnu.org/software/make/\">GNU Make</a> commands from the\nproject root directory.</p>"}
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
