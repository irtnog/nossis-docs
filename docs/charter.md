% Nossis Docs, serverless hosting for static, private web sites
%
% Copyright (C) 2024-2025  Matthew X. Economou
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU Affero General Public License as
% published by the Free Software Foundation, either version 3 of the
% License, or (at your option) any later version.
%
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
% Affero General Public License for more details.
%
% You should have received a copy of the GNU Affero General Public
% License along with this program.  If not, see
% <https://www.gnu.org/licenses/>.

# Project Charter

Refer to
["Project Charter - Agile Project"](http://web.archive.org/web/20100412014125/http://analytical-mind.com/2009/08/12/project-charter-agile-project/),
["What Should an Agile Project Charter Contain?"](https://www.infoq.com/news/2010/05/agile-project-charter/),
and
["A Guide to the Project Priorities (Prioritization) Matrix"](https://www.indeed.com/career-advice/career-development/project-priorities-matrix)
for additional guidance.

## Vision

> Why do this work?  What challenges do we face?

Static, private web site hosting should be too cheap to meter.
: However, hosting services take advantage of organizations that lack
  the requisite expertise to self-host this kind of content by
  requiring costly "business-class" or "enterprise" service plans.

Static, private web site hosting should be secure.
: However, hosting services generally lack recognized information
  security accrediations, or if they are accredited, it is for
  low-impact workloads only.

Static, private web site hosting should be federated.
: However, hosting services limit access to licensed users of the
  hosting service itself.  Single sign-on (SSO), if available, is
  limited to Big Tech companies' identity providers, with bilateral
  SAML or OIDC integrations locked behind an enterprise sales funnel.
  True multilateral authentication and authorization, whether via SAML
  or OpenID federations, is almost never supported, limiting
  cross-organization collaboration.

## Objectives

> What will this project do?  What's our mission?

Self-publish static, private web sites from dedicated branches in
GitHub repositories---similar to GitHub Pages---using Amazon S3 and a
compatible OpenID Connect (OIDC) identity provider.

## Success Criteria

> What effects or outcomes should this project have?

- Serverless infrastructure as code

- Secure by default

- Federated single sign-on

## Project Priorities

> How is this project constrained?

|                                 | Time<br>(Schedule) | Cost<br>(Budget) | Scope<br>(Boundary) |
|--------------------------------:|:------------------:|:----------------:|:-------------------:|
|   Constrain<br>(Not negotiable) |                    | ✅               |                     |
| Accept<br>(Difficult to Change) |                    |                  | ✅                  |
|         Enhance<br>(Negotiable) | ✅                 |                  |                     |

## Risks

> What might make the project exceed a constraint or alter a priority?

% TODO

## Stakeholders

> Who depends on the project's success?

% TODO
