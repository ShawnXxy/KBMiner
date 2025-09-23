<a id="readme-top"></a>

<!-- LANGUAGE SWITCH -->
---



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/ShawnXxy/KBMiner">
    <img src="images/logo.png" alt="Logo" width="25%" height="auto">
  </a> -->

<h3 align="center">KBMiner</h3>

  <p align="center">
    KBMiner is a command-line tool for automatically crawling, filtering, indexing, and archiving MySQL-related technical articles from ActionTech and Alibaba's official sources. Built in Python with a modular, extensible crawler framework, it supports incremental and full crawls, keyword-based filtering, Markdown indexing, HTML-to-Markdown conversion, and robust state management for resumable operations. The tool provides unified, customizable mining of technical knowledge base content for database professionals.
    <br />
    <a href="https://github.com/ShawnXxy/KBMiner"><strong>Explore the docs »</strong></a>
    <br />
  </p>

  <!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!-- [![Latest Release][release-shield]][release-url]
![Release Date][release-date-shield] -->
[![License][license-shield]][license-url]

  <p align="center">
    <a href="https://github.com/ShawnXxy/KBMiner">View Demo</a>
    &middot;
    <a href="https://github.com/ShawnXxy/KBMiner/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ShawnXxy/KBMiner/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 📖 About The Project

[![Flow Chart](images/flow.png)](https://example.com)

KBMiner is a command-line tool for automatically crawling, filtering, indexing, and archiving MySQL-related technical articles from ActionTech and Alibaba's official sources. Built in Python with a modular, extensible crawler framework, it supports incremental and full crawls, keyword-based filtering, Markdown indexing, HTML-to-Markdown conversion, and robust state management for resumable operations. The tool provides unified, customizable mining of technical knowledge base content for database professionals.

### Key Features

- **Unified multi-source crawling:** Aggregates MySQL-related content from both ActionTech and Alibaba sources through a single interface.
- **Incremental & full crawl support:** Choose between updating only new/uncompleted items or rebuilding the entire index from scratch.
- **Keyword-based content filtering:** Includes/excludes articles based on title and category keywords for precise topic targeting.
- **Markdown article indexing:** Organizes collected articles in Markdown files, categorized by source and time, for easy browsing.
- **Local article downloading & conversion:** Downloads full article content and converts HTML to Markdown, saving it locally alongside referenced images.
- **Robust logging & error handling:** Detailed logs, error resilience, and resumable state management for reliable operation.
- **Extensible crawler architecture:** Modular design allows easy extension to new sources or custom filtering and output logic.
- **Portable & dependency-free:** Relies solely on the Python standard library—no external packages required.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### 📁 Project Structure

<details>
<summary>Click to expand project structure</summary>

```
KBMiner/
├── .flake8
├── .gitignore
├── miner.py
├── crawlers/
│   ├── actiontech_crawler.py
│   ├── ali_crawler.py
│   ├── base_crawler.py
│   ├── mysql_crawler.py
├── kb/
│   ├── my/
│   │   ├── actiontech/
│   │   │   ├── crawl_state.json
│   │   │   ├── articles/
│   │   │   │   ├── .img/
│   │   ├── ali_monthly/
│   │   │   ├── .processed_months.txt
│   │   │   ├── articles/
│   │   │   │   ├── .img/
│   │   ├── my_manual/
│   │   │   ├── refman-5.7-en.pdf
│   │   │   ├── refman-8.0-en.pdf
│   │   │   ├── refman-8.4-en.pdf
│   │   │   ├── docs_md/
│   │   │   │   ├── 57/
│   │   │   │   ├── 80/
│   │   │   │   ├── 84/
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## 🚀 Getting Started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.7 or above (standard library only; no external dependencies)
- Stable internet connection (required for crawling source websites)
- Sufficient disk space (knowledge base directories can grow large due to article and image storage)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShawnXxy/KBMiner.git
   cd KBMiner
   ```

2. **(Optional) Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **No further installation is required. KBMiner does not rely on external packages.**

### Configuration

- By default, the knowledge base and downloaded articles will be stored within the `kb/my/` directory.
- You can customize crawl options (incremental/full, source selection, etc.) at runtime via command-line arguments.
- For best results, review the `miner.py` script and the output structure in `kb/my/` to understand how content is organized.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## 💻 Usage

The main entry point is `miner.py`. Run it directly with Python:

```bash
python miner.py [OPTIONS]
```

**Common options:**

- `--asset {actiontech,ali_monthly,all}` : Select which source(s) to crawl (`all` is default).
- `--full` : Force a full crawl (rebuild the entire index from scratch).
- `--incremental` : Only update new/uncompleted articles (default behavior).
- `--download` : Download full article content and save locally.
- `--download-only` : Only download articles for already indexed entries.
- `--test` : Run in test mode with limited crawling (for safe/quick checks).
- `--test-articles N` : Only process the first N articles for testing.
- `--verbose` / `--quiet` : Control logging output level.

**Examples:**

- Incremental crawl both sources, index only (no download):
  ```bash
  python miner.py --asset all --incremental
  ```

- Full crawl and download for ActionTech only:
  ```bash
  python miner.py --asset actiontech --full --download
  ```

- Download missing articles for Alibaba monthly, skipping crawl:
  ```bash
  python miner.py --asset ali_monthly --download-only
  ```

- Run a test crawl of 5 articles from both sources:
  ```bash
  python miner.py --test-articles 5
  ```

**Resulting files and articles will appear in the respective directories under `kb/my/`. Logs and summaries are printed to the console.**

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## 🗺️ Roadmap

- [x] Unified multi-source crawling (ActionTech, Alibaba)
- [x] Incremental and full crawl support
- [x] Markdown index generation and organization by category/month
- [x] Article content download and HTML-to-Markdown conversion
- [x] Robust keyword-based filtering (allow/deny lists)
- [x] Logging, error handling, and resumable state management
- [ ] Support for additional knowledge base sources (future)
- [ ] Configurable output locations and advanced filtering
- [ ] Web or GUI front-end for browsing archived articles

See the [open issues](https://github.com/ShawnXxy/KBMiner/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/ShawnXxy/KBMiner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ShawnXxy/KBMiner" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## 🎗 License

Copyright © 2024-2025 [KBMiner][KBMiner].  
Released under the [MIT][license-url] license.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## 📧 Contact

Email: your.email@example.com

Project Link: [https://github.com/ShawnXxy/KBMiner](https://github.com/ShawnXxy/KBMiner)

This project is designed to operate without external Python dependencies, relying solely on the standard library, making it highly portable and easy to set up. For best results, ensure you have stable internet connectivity during crawling, and note that the knowledge base directories can grow significantly in size due to the storage of article content and images.

<p align="right">(<a href="#readme-top">back to top</a>)</p>







<!-- REFERENCE LINKS -->
[KBMiner]: https://github.com/ShawnXxy/KBMiner

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ShawnXxy/KBMiner.svg?style=flat-round
[contributors-url]: https://github.com/ShawnXxy/KBMiner/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ShawnXxy/KBMiner.svg?style=flat-round
[forks-url]: https://github.com/ShawnXxy/KBMiner/network/members
[stars-shield]: https://img.shields.io/github/stars/ShawnXxy/KBMiner.svg?style=flat-round
[stars-url]: https://github.com/ShawnXxy/KBMiner/stargazers
[issues-shield]: https://img.shields.io/github/issues/ShawnXxy/KBMiner.svg?style=flat-round
[issues-url]: https://github.com/ShawnXxy/KBMiner/issues
[release-shield]: https://img.shields.io/github/v/release/ShawnXxy/KBMiner?style=flat-round
[release-url]: https://github.com/ShawnXxy/KBMiner/releases
[release-date-shield]: https://img.shields.io/github/release-date/ShawnXxy/KBMiner?color=9cf&style=flat-round
[license-shield]: https://img.shields.io/github/license/ShawnXxy/KBMiner.svg?style=flat-round
[license-url]: https://github.com/ShawnXxy/KBMiner/blob/master/LICENSE.txt

[Python]: https://img.shields.io/badge/Python-3776AB?style=flat-round&logo=python&logoColor=white
[Python-url]: https://www.python.org/