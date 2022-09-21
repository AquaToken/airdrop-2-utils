<div id="top"></div>


<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AquaToken/airdrop-2-utils">
    <img src="https://aqua.network/assets/img/header-logo.svg" alt="Logo" width="250" height="80">
  </a>

<h3 align="center">Aquarius Airdrop 2 Utils</h3>

  <p align="center">
    Aquarius protocol is governed by DAO voting with AQUA tokens. Vote and participate in discussions to shape the future of Aquarius.
    <br />
    <br />
    <a href="https://github.com/AquaToken/airdrop-2-utils/issues">Report Bug</a>
    ·
    <a href="https://vote.aqua.network/">Request Feature</a>
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
        <li><a href="#development-server">Development server</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Airdrop 2 Screen Shot][product-screenshot]](https://aqua.network/airdrop2)


#### AQUA Airdrop #2 Utils
Unlike the initial airdrop, eligibility for airdrop #2 is not defined from a snapshot of a past ledger.
This application collects all the required information for airdrop, using stellar core database which should be synchronized up to desired ledger.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://python.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Stellar SDK](https://pypi.org/project/stellar-sdk/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

### Prerequisites
Project requires stellar core to be synchronized up to desired ledger.
This can be achieved using `stellar-core catchup DESTINATION-LEDGER/1` command.
https://developers.stellar.org/docs/run-core-node/commands#command-line-options

#### Clone project
`git clone git@github.com:AquaToken/airdrop-2-utils.git`

#### Create environment & install requirements
`pipenv sync --dev`

#### Run snapshot command
`pipenv run python snapshot.py --db="<stellar_core_database_url>" --output=snapshot.csv`

#### Done
Snapshot file will be generated as `snapshot.csv` and can be consumed by corresponding api: https://github.com/AquaToken/aqua-airdrop-2-checker-api


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Email: [hello@aqua.network](mailto:hello@aqua.network)
Telegram chat: [@aquarius_HOME](https://t.me/aquarius_HOME)
Telegram news: [@aqua_token](https://t.me/aqua_token)
Twitter: [@aqua_token](https://twitter.com/aqua_token)
GitHub: [@AquaToken](https://github.com/AquaToken)
Discord: [@Aquarius](https://discord.gg/sgzFscHp4C)
Reddit: [@AquariusAqua](https://www.reddit.com/r/AquariusAqua/)
Medium: [@aquarius-aqua](https://medium.com/aquarius-aqua)

Project Link: [https://github.com/AquaToken/airdrop-2-utils](https://github.com/AquaToken/airdrop-2-utils)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/AquaToken/airdrop-2-utils.svg?style=for-the-badge
[contributors-url]: https://github.com/AquaToken/airdrop-2-utils/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/AquaToken/airdrop-2-utils.svg?style=for-the-badge
[forks-url]: https://github.com/AquaToken/airdrop-2-utils/network/members
[stars-shield]: https://img.shields.io/github/stars/AquaToken/airdrop-2-utils.svg?style=for-the-badge
[stars-url]: https://github.com/AquaToken/airdrop-2-utils/stargazers
[issues-shield]: https://img.shields.io/github/issues/AquaToken/airdrop-2-utils.svg?style=for-the-badge
[issues-url]: https://github.com/AquaToken/airdrop-2-utils/issues
[license-shield]: https://img.shields.io/github/license/AquaToken/airdrop-2-utils.svg?style=for-the-badge
[license-url]: https://github.com/AquaToken/airdrop-2-utils/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
