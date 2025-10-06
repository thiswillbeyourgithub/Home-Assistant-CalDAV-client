from caldav_tasks_api.caldav_tasks_api import TasksAPI, TaskData

@service
def caldav_add(
    summary: str,
    list_uid: str,
    url: str,
    username: str,
    password: str,
    priority: int = 3,
    description: str = "",
    debug: bool = False,
):
    """yaml
description: Create a new CalDAV task
fields:
    summary:
        description: Task summary/title
        example: "Buy groceries"
        required: true
        selector:
            text:
    priority:
        description: Task priority on a 0 to 10 scale
        example: 5
        required: false
        default: 3
        selector:
            number:
                min: 0
                max: 10
    description:
        description: Task description
        example: "Important before the wedding"
        required: false
        default: ""
        selector:
            text:
    list_uid:
        description: Target task list UID
        example: "groceries"
        required: true
        default: "perso"
        selector:
            text:
    url:
        description: CalDAV server URL
        example: "https://nextcloud.example.com/remote.php/dav"
        required: true
        selector:
            text:
    username:
        description: CalDAV username
        example: "user@example.com"
        required: true
        selector:
            text:
    password:
        description: CalDAV password
        required: true
        selector:
            text:
    debug:
        description: Enable debug logging
        default: false
        selector:
            bool:
    """
    log.info(f"CaldavTasksAPI: will create task '{summary}' in list '{list_uid}'")
    assert url, "caldav url not specified"
    assert password, "caldav password not specified"
    assert username, "caldav username not specified"
    assert list_uid, "caldav list_uid not specified"
    assert priority, "caldav priority not specified"

    api = task.executor(
        TasksAPI,
        url=url,
        username=username,
        password=password,
        nextcloud_mode=True,
        debug=debug,
    )
    status = task.executor(
        api.add_task,
        task_data=TaskData(
            summary=summary,
            list_uid=list_uid,
            priority=priority,
            description=description,
        ),
        list_uid=list_uid,
    )
    log.info(f"Created task. Status: '{str(status)}'")
    return status
