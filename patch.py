import re

with open('preview-312.html', 'r') as f:
    preview = f.read()

with open('index.html', 'r') as f:
    index = f.read()

# 1. Extract CSS
css_match = re.search(r'(\.scene\{.*?\n\.screen__chat \.img-blur\{\n  opacity: calc\(var\(--p-zoom\) \* 50\);\n\})', preview, re.DOTALL)
if not css_match:
    print("Could not find CSS block in preview")
    exit(1)
new_css = css_match.group(1)

# Replace in index
index = re.sub(r'\.scene\{.*?\n\.screen__chat\{.*?-webkit-text-size-adjust: none;\n  text-size-adjust: none;\n\}', new_css, index, flags=re.DOTALL)


# 2. Extract HTML
html_match = re.search(r'(<section class="scene js-scene" aria-label="Office chaos, then the chat teach-through">.*?</section>\n\n<section class="scene js-scene" aria-label="Office chaos, then the chat teach-through">.*?</section>)', preview, re.DOTALL)
if not html_match:
    print("Could not find HTML block in preview")
    exit(1)
new_html = html_match.group(1)

# Replace in index
index = re.sub(r'<section class="scene js-scene" aria-label="Office chaos, then the chat reveal">.*?</section>', new_html, index, flags=re.DOTALL)


# 3. Extract JS
js_match = re.search(r'(function initSceneZoom\(\)\{.*?)window\.addEventListener\(\'scroll\', \(\) => \{', preview, re.DOTALL)
if not js_match:
    print("Could not find JS block in preview")
    exit(1)
new_js = js_match.group(1)

# Replace in index
index = re.sub(r'  // Compute exact chat zoom vars from rendered layout.*?if\(hero && !prefersReduced\)\{', new_js + '  const hero = document.querySelector(\'.hero\');\n  if(hero && !prefersReduced){', index, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(index)

print("Patched successfully")
