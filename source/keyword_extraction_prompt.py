def contruct_prompt(issue):
    # prompt = f"""
    # You are a Technical Keyword Extraction Assistant.  
    # Given a GitHub issue’s **Title** and **Description**, extract a concise list of the **most important technical keywords**.  
    # - **Only** include terms that refer to filenames, module or class names, function/method names, error types, CamelCase identifiers, configuration keys, library names, etc.  
    # - **Do not** include vague words (e.g. "problem", "issue", "error" by itself, "performance", "slow", etc.) unless they are part of a specific technical identifier (e.g. `NullPointerException`).  
    # - Preserve original casing and punctuation for CamelCase or dotted names.  
    # - Return your answer as a JSON array under the key `keywords`.

    # ### Format:

    # keywords: \[
    # "FirstKeyword",
    # "Another\_Term",
    # "someLibrary.js",
    # "ModuleName.methodName()",
    # …
    # ]

    # ### Few-Shot Examples

    # #### Example 1
    # **Input**  
    # Title: `NullPointerException in DataProcessor.processData when input is null`  
    # Description: `I’m seeing a NullPointerException thrown from the DataProcessor.processData method whenever the input parameter is null.  
    # Stack trace shows com.example.dataprocessor.DataProcessor.processData(DataProcessor.java:45).`

    # **Output**  
    # [
    # "NullPointerException",
    # "DataProcessor.processData",
    # "com.example.dataprocessor.DataProcessor",
    # "DataProcessor.java"
    # ]

    # #### Example 2
    # **Input**  
    # Title: `React UI freeze when clicking SaveButton in production build`  
    # Description: `After deploying the React app, clicking the SaveButton component causes the UI to lock up.  
    # The issue appears in SaveHandler.handleSave() and only reproduces in the production webpack bundle.`

    # **Output**  
    # [
    # "React",
    # "SaveButton",
    # "SaveHandler.handleSave()",
    # "production webpack bundle"
    # ]

    # #### Example 3
    # **Input**  
    # Title: `Memory leak in CacheManager.close() method`  
    # Description: `When shutting down the service, CacheManager.close() does not release file handles, leading to a memory leak detected by VisualVM.  
    # I’m using version 2.3.1 of cache-lib.`

    # **Output**  
    # [
    # "CacheManager.close()",
    # "file handles",
    # "memory leak",
    # "VisualVM",
    # "cache-lib 2.3.1"
    # ]

    # **Now apply the same extraction logic to the new issue below:**  

    # Title: {issue['title']}
    # Description: {issue['body']}
    # """

    # return prompt

    prompt = f"""
    You are a Technical Keyword & Issue Summary Extraction Assistant.

    Given a GitHub issue’s **Title**, **Description**, and **Labels**, you must produce:

    1. A JSON array `keywords` containing only the most important **technical** terms:
    - Filenames, module/class names, function/method names, error types, CamelCase identifiers, config keys, library names, etc.
    - Preserve original casing and punctuation.
    - **Do not** include vague words like “issue,” “problem,” “performance,” unless part of a specific identifier (e.g. `NullPointerException`).

    2. A **50-word max** natural-language `summary` of the issue, synthesizing title, description, and labels.

    Return exactly this JSON structure:

    ```json
    {{
    "keywords": [ … ],
    "summary": "…"
    }}
    ````

    ### Few-Shot Examples

    #### Example 1

    **Input**
    Title: `NullPointerException in DataProcessor.processData when input is null`
    Description:
    I’m seeing a NullPointerException thrown from the DataProcessor.processData method whenever the input parameter is null.
    Stack trace shows com.example.dataprocessor.DataProcessor.processData(DataProcessor.java:45).
    Labels: `[ "bug", "high-priority" ]`

    **Output**
    ```json
    {{
    "keywords": [
        "NullPointerException",
        "DataProcessor.processData",
        "com.example.dataprocessor.DataProcessor",
        "DataProcessor.java"
    ],
    "summary": "Users encounter a NullPointerException in DataProcessor.processData when a null input is passed. The stack trace pinpoints com.example.dataprocessor.DataProcessor.processData in DataProcessor.java:45. This crash must be mitigated by adding null checks or input validation before processing."
    }}
    ```

    #### Example 2

    **Input**
    Title: `React UI freeze when clicking SaveButton in production build`
    Description:
    After deploying the React app, clicking the SaveButton component causes the UI to lock up.
    The issue appears in SaveHandler.handleSave() and only reproduces in the production webpack bundle.
    Labels: `[ "bug", "UI", "production" ]`

    **Output**
    ```json
    {{
    "keywords": [
        "React",
        "SaveButton",
        "SaveHandler.handleSave()",
        "production webpack bundle"
    ],
    "summary": "In the production webpack bundle, clicking the SaveButton in the React app causes the UI to freeze. Investigation shows SaveHandler.handleSave() hangs only in the optimized build. This regression blocks user actions after deploy and requires debugging the handler or adjusting the build configuration."
    }}
    ```

    #### Example 3

    **Input**
    Title: `Memory leak in CacheManager.close() method`
    Description:
    When shutting down the service, CacheManager.close() does not release file handles,
    leading to a memory leak detected by VisualVM.
    I’m using version 2.3.1 of cache-lib.
    Labels: `[ "performance", "memory" ]`

    **Output**
    ```json
    {{
    "keywords": [
        "CacheManager.close()",
        "file handles",
        "memory leak",
        "VisualVM",
        "cache-lib 2.3.1"
    ],
    "summary": "CacheManager.close() fails to release file handles during service shutdown, causing a memory leak detected by VisualVM. This occurs in cache-lib version 2.3.1 and degrades performance over time. Ensuring proper resource cleanup in CacheManager.close() is essential to prevent system instability."
    }}
    ```

    **Now process the new issue below using the same rules:**

    ```
    Title: {issue['title']}
    Description: {issue['body']}
    Labels: {issue['labels']}
    ```
    """

    return prompt



# Old prompt

# prompt = f"""
# Role:
# You are an expert open-source project maintainer. Your job is to extract the most important technical keywords from GitHub issues.
# Focus on technical terms, filenames, modules, functions, error types, and important features.
# If the issue description is vague or unclear, make an intelligent guess based on common software engineering knowledge, but stay conservative.
# Input:
# You are given the title and description of a GitHub issue. The description may be detailed or vague.
# Steps:
# - Read the title and description carefully.
# - Focus on extracting technical keywords, such as:
#     - Technical components (e.g., SSH, API, logging)
#     - Programming languages or frameworks
#     - Infrastructure components (e.g., cloud storage, servers)
#     - Specific error types
#     - Filenames, file paths, or modules if mentioned
#     - Important features or version information
#     - The keywords should be single words or words with "-"
# - If the description is vague or missing technical terms, make an intelligent guess based on common software engineering knowledge, but stay conservative.
# - Only return keywords that are explicitly present or strongly implied.
# - Do not include random words, general English, or anything unrelated.

# Expectations:
# - Output only comma-separated keywords.
# - No extra explanation, sentences, or formatting.
# - If no technical keywords are found, return an empty string.

# Example:

# ---
# Example Input:

# Title:  "Reduce integration test dependencies on external resources"

# Body:"### Summary\n\nMany integration tests depend on external resources, aside from pip installed packages from PyPI and OS package installs. These dependencies should be replaced with local options where possible.\n\nExamples of dependencies to consider replacing:\n\n- File downloads, such as from the ci-files S3 bucket.\n\n- Use of external APIs, such as Galaxy.\n\n- Cloning of git repositories, usually from GitHub.\n\n- Installation of packages from alternative repositories.\n\nChanges should be backported through stable-2.14, when possible, particularly for tests run on RHEL..\n\n\n\n### Issue Type\n\nFeature Idea\n\n### Component Name\n\nintegration tests\n\n### Ansible Version\n\n```console\n$ ansible --version\n```\n\n### Configuration\n\n```console\n### OS / Environment\n\nlinux\n\n### Additional Information\n\n.\n\n### Code of Conduct\n\n- [x] I agree to follow the Ansible Code of Conduct"

# Expected Keywords/Output:
# integration-tests, external-dependencies, S3, bucket, ci-files, Galaxy, API, Git, package, repositories, RHEL, backporting, Stable-2.14, dependency-isolation, Feature, 

# ---
# Analyze this GitHub issue and extract relevant technical keywords:
# New Input:

# Title: {issue['title']}
# Description: {issue['body']}

# Extract and return only comma-separated technical keywords.
# """