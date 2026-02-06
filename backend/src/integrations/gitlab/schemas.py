from pydantic import BaseModel, ConfigDict


class _GitLabBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class GitLabProject(_GitLabBase):
    id: int
    name: str
    path: str
    path_with_namespace: str
    ssh_url_to_repo: str
    http_url_to_repo: str
    web_url: str
    default_branch: str | None = None
    visibility: str


class GitLabBranch(_GitLabBase):
    name: str
    merged: bool = False
    protected: bool = False
    web_url: str | None = None


class BranchAccessLevel(_GitLabBase):
    id: int | None = None
    access_level: int | None = None
    access_level_description: str | None = None


class GitLabProtectedBranch(_GitLabBase):
    id: int
    name: str
    push_access_levels: list[BranchAccessLevel] = []
    merge_access_levels: list[BranchAccessLevel] = []
    allow_force_push: bool = False
    code_owner_approval_required: bool = False


class GitLabCommit(_GitLabBase):
    id: str
    short_id: str
    title: str
    message: str
    author_name: str
    web_url: str | None = None


class GitLabApprovalConfiguration(_GitLabBase):
    approvals_before_merge: int
    reset_approvals_on_push: bool
    disable_overriding_approvers_per_merge_request: bool
    merge_requests_author_approval: bool


class GitLabMember(_GitLabBase):
    id: int
    username: str
    name: str
    state: str
    access_level: int
    web_url: str | None = None


class GitLabUser(_GitLabBase):
    id: int
    username: str
    name: str
    state: str
    avatar_url: str | None = None
    web_url: str | None = None
