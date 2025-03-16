document.addEventListener("DOMContentLoaded", () => {
    const tasks = document.querySelectorAll(".task");
    const taskLists = document.querySelectorAll(".task-list");

    tasks.forEach(task => {
        task.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("task_id", task.dataset.id);
        });
    });

    taskLists.forEach(list => {
        list.addEventListener("dragover", (e) => {
            e.preventDefault();
        });

        list.addEventListener("drop", async (e) => {
            e.preventDefault();
            const taskId = e.dataTransfer.getData("task_id");
            const newStatus = list.id;

            await fetch("/update_status", {
                method: "POST",
                body: new URLSearchParams({ "task_id": taskId, "new_status": newStatus }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });

            location.reload();
        });
    });
});

function deleteTask(taskId) {
    window.location.href = `/delete/${taskId}`;
}
