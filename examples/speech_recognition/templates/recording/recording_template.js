exports.Task = extend(TolokaHandlebarsTask, function (options) {
    TolokaHandlebarsTask.call(this, options);
}, {
    onRender: function() {
        // DOM element for task is formed (available via #getDOMElement())
        var $el = $(this.getDOMElement());

        this._getFile = this.file.getFile;
        this.file.getFile = function() {
            this.focus();

            return this._getFile.apply(this.file, arguments);
        }.bind(this);

        const root = this.getDOMElement();

        if (!this.getWorkspaceOptions().isReviewMode && !this.getWorkspaceOptions().isReadOnly) {
            const label = root.querySelector('label.field_file__label');
            const icon = label.querySelector('i.icon');
            const text = root.querySelector('span.field_file__upload');
            const files = root.querySelector('div.field_file__files');

            label.onclick = () => {
                icon.style.backgroundImage = 'url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMSIgeD0iMCIgeT0iMCIgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiB2aWV3Qm94PSIwIDAgNjQgNjQiIHhtbDpzcGFjZT0icHJlc2VydmUiPjxwYXRoIHN0eWxlPSJmaWxsOiMzMTlEMDAiIGQ9Ik0zMiAwQzE0LjMgMCAwIDE0LjMgMCAzMnMxNC4zIDMyIDMyIDMyIDMyLTE0LjMgMzItMzJTNDkuNyAwIDMyIDB6TTMyIDYyQzE1LjQgNjIgMiA0OC42IDIgMzIgMiAxNS40IDE1LjQgMiAzMiAyYzE2LjYgMCAzMCAxMy40IDMwIDMwQzYyIDQ4LjYgNDguNiA2MiAzMiA2MnoiLz48cGF0aCBzdHlsZT0iZmlsbDojMzE5RDAwIiBkPSJNMzIgMzdjMy4zIDAgNi0yLjcgNi02di05YzAtMy4zLTIuNy02LTYtNiAtMy4zIDAtNiAyLjctNiA2djlDMjYgMzQuMyAyOC43IDM3IDMyIDM3ek0yOCAyMmMwLTIuMiAxLjgtNCA0LTRzNCAxLjggNCA0djljMCAyLjItMS44IDQtNCA0cy00LTEuOC00LTRWMjJ6TTQyIDMxYzAtMC42LTAuNC0xLTEtMXMtMSAwLjQtMSAxYzAgNC40LTMuNiA4LTggOHMtOC0zLjYtOC04YzAtMC42LTAuNC0xLTEtMXMtMSAwLjQtMSAxYzAgNS4yIDMuOSA5LjQgOSA5LjlWNDZoLTNjLTAuNiAwLTEgMC40LTEgMXMwLjQgMSAxIDFoOGMwLjYgMCAxLTAuNCAxLTFzLTAuNC0xLTEtMWgtM3YtNS4xQzM4LjEgNDAuNCA0MiAzNi4yIDQyIDMxeiIvPjwvc3ZnPg==)'
                text.style.color = '#319D00';
                text.textContent = 'Recording';
            }

            files.addEventListener("click", () => {
                const fileDelete = files.querySelector('div.file__delete');
                fileDelete.onclick = () => {
                    icon.style.backgroundImage = 'url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMSIgeD0iMCIgeT0iMCIgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiB2aWV3Qm94PSIwIDAgNjQgNjQiIHhtbDpzcGFjZT0icHJlc2VydmUiPjxwYXRoIGQ9Ik0zMiAwQzE0LjMgMCAwIDE0LjMgMCAzMnMxNC4zIDMyIDMyIDMyIDMyLTE0LjMgMzItMzJTNDkuNyAwIDMyIDB6TTMyIDYyQzE1LjQgNjIgMiA0OC42IDIgMzIgMiAxNS40IDE1LjQgMiAzMiAyYzE2LjYgMCAzMCAxMy40IDMwIDMwQzYyIDQ4LjYgNDguNiA2MiAzMiA2MnoiLz48cGF0aCBkPSJNMzIgMzdjMy4zIDAgNi0yLjcgNi02di05YzAtMy4zLTIuNy02LTYtNiAtMy4zIDAtNiAyLjctNiA2djlDMjYgMzQuMyAyOC43IDM3IDMyIDM3ek0yOCAyMmMwLTIuMiAxLjgtNCA0LTRzNCAxLjggNCA0djljMCAyLjItMS44IDQtNCA0cy00LTEuOC00LTRWMjJ6TTQyIDMxYzAtMC42LTAuNC0xLTEtMXMtMSAwLjQtMSAxYzAgNC40LTMuNiA4LTggOHMtOC0zLjYtOC04YzAtMC42LTAuNC0xLTEtMXMtMSAwLjQtMSAxYzAgNS4yIDMuOSA5LjQgOSA5LjlWNDZoLTNjLTAuNiAwLTEgMC40LTEgMXMwLjQgMSAxIDFoOGMwLjYgMCAxLTAuNCAxLTFzLTAuNC0xLTEtMWgtM3YtNS4xQzM4LjEgNDAuNCA0MiAzNi4yIDQyIDMxeiIvPjwvc3ZnPg==)'
                    text.style.color = 'black';
                    text.textContent = 'Recording';
                }
            }, true);
        }
    },
    focus: function() {
        this.getView().$el.siblings().removeClass('task_focused');
        this.getView().$el.addClass('task_focused');
        this.getView().$el.scrollintoview();

        this.onFocus();
    },
    getTemplateData: function() {
        // Play audio in task review mode
        var data = TolokaHandlebarsTask.prototype.getTemplateData.apply(
            this,
            arguments
            ),
            input = this.getTask().input_values,
            reviewMode = this.getWorkspaceOptions().isReviewMode || this.getWorkspaceOptions().isReadOnly,
            task = this;

        if (reviewMode) {
            var audio = '',
                output = task.getOptions().solution.output_values;

            audio = task.getWorkspaceOptions().apiOrigin + '/api/attachments/' + output.audio_record + '/preview';
            data.audio = audio;
            data.reviewMode = true;
        }
        return data;
    }
});


exports.TaskSuite = extend(TolokaHandlebarsTaskSuite, function (options) {
    TolokaHandlebarsTaskSuite.call(this, options);
}, {
    onRender: function() {
        this.getFocusedTask() && this.getFocusedTask().blur();

        window.onresize = function(event) {
            var iter = 0,
                timerId = setInterval(function() {
                    if (iter > 4) {
                        clearInterval(timerId);
                    }

                    this.get$Element().find('.task_focused').scrollintoview();
                    iter++;
                }.bind(this), 50);
        }.bind(this);
    },
    focusTask: function() {
    },
    onDestroy: function() {
    }
});


function extend(ParentClass, constructorFunction, prototypeHash) {
    constructorFunction = constructorFunction || function () {};
    prototypeHash = prototypeHash || {};
    if (ParentClass) {
        constructorFunction.prototype = Object.create(ParentClass.prototype);
    }
    for (var i in prototypeHash) {
        constructorFunction.prototype[i] = prototypeHash[i];
    }
    return constructorFunction;
}
