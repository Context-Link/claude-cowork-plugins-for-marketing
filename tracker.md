I want to put together a 'marketplace called "Claude Cowork plugins for Marketing". 
Official plugins doc here: https://code.claude.com/docs/en/plugins.md
Official plugins marketplace doc here: https://code.claude.com/docs/en/plugin-marketplaces

This directory stores the plugins for the market place. 
My intention is to include our plugin (Context Link), but also other marketing plugins from the community.
We need to convert the below repos to Plugins so they can use Claude Cowork.
When we put together this gallery it's important to link to the official source for each plugin. I want this to be a curated list of high-quality plugins, not us replacing/stealing the official sources.

I've started the marketplace file here /.claude-plugin/marketplace.json
And the plugins are in ./plugins

We will use this folder to track the plugins we want to include in the market place.


## Plugin List

### Context Link
Ready to include: true
official URL: https://github.com/oliwoodsuk/context-link-plugin

- name:
- description:
- version

### marketing (by-anthropic)
Ready to include: true
official URL: https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing

- name:
- description:
- version

### Marketing Skills (By Corey of Conversion Factory)
Ready to include: true - (Already a plugin)
official URL: https://github.com/coreyhaines31/marketingskills (Coreys marketplace: https://github.com/coreyhaines31/marketingskills/blob/main/.claude-plugin/marketplace.json)

- name:
- description:
- version

### dataforseo(nikhil-bhansali)
Ready to include: false - Needs converting from one Skill to many skills, also possibly need to add to individual skill files a prompt to ask for data-seo credentrials.
official URL: https://github.com/nikhilbhansali/dataforseo-skill-claude/tree/master

- name:
- description:
- version

### seo-machine-skills(by-craig-hewitt)
Ready to include: false (seo-machine(by-craig-hewitt) contains the full git repo, with .claude dir)
This is a big one, there's important markdown files in context/ that I think needs generating via a new /setup-seo-machine command. 
There are also important scripts in data_sources/ that need to be included in the individual scripts folders (official URL on Claude skills here: https://code.claude.com/docs/en/skills.md)

official URL: https://github.com/TheCraigHewitt/seomachine

- name:
- description:
- version


## Changelog
