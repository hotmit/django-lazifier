from collections import OrderedDict
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.json.json import Json


class Ajx:
    # region [ enums ]
    class DisplayMethod:
        none = 'none'
        bs_dialog = 'bs-dialog'
        block_ui = 'block-ui'
        alert = 'alert'

    class Status:
        success = 'success'
        error = 'error'

    # region [ Command ]
    class Command:
        none = 'none'
        refresh = 'refresh'
        """
        Refresh the page (ie. use js to call browser refresh)
        """

        redirect = 'redirect'
        """
        Use javascript to redirect to another url
        """

        ajax_refresh = 'ajax-refresh'
        """
        Load the current page using ajax, and grab the content and refresh the target section.
        """

        ajax_get = 'ajax-get'
        """
        Similar to ajax-refresh but instead of current page, use another specific page.
        """

        ajax_post = 'ajax-post'
        """
        Post to another url and grab the content to update current page section
        """

        replace_html = 'replace-html'
        """
        Replace a target section of the current page with the html in data
        """

        append_html = 'append-html'

    # endregion

    class BsDialogType:
        default = 'type-default'
        info = 'type-info'
        primary = 'type-primary'
        success = 'type-success'
        warning = 'type-warning'
        danger = 'type-danger'

    class BsDialogSize:
        normal = 'size-normal'
        wide = 'size-wide'
        large = 'size-large'

    # endregion

    @classmethod
    def send_ajax_command(cls, message: str = '', display_method='block-ui',
                          command='none', status='success',
                          js_on_pre_parse: str = '', js_on_post_parse: str = '', js_on_ajax_success: str = '',
                          **options):
        """
        Tell the recipient to display the message on screen.
        Once the message is displayed either refresh, redirect or do nothing.

        Support kwargs: all keys in options will be convert to js naming standard (camel case) remote_url => remoteUrl
                redirect:
                    redirect_url {!url}: the redirect url

                ajax-refresh:
                    common_target {!selector}: both local and remote html element, if this is specified
                                                then local_target and remote_target will be overwritten

                    local_target {!selector=}:  the local html element
                    remote_target {!selector=}: the remote html element

                ajax-get, ajax-post:
                    local_target {!selector}: the local html element
                    remote_url {!url}: the remote url to retrieve the content
                    remote_target {?selector}: the remote html element, if none then use the entire content
                    data {!dict=}: the data for the post or the get ajax call

                replace-html, append-html:
                    local_target {!selector}
                    html_content {!html}: the html to be use as the replacement
                    content_selector {?selector}

                ===
                // Method

                block-ui:
                    overlayCSS {dict=}: css overlay for $.blockUI - None use default overlay
                    blockTarget {string=}: css selector for the element
                                            to cover the message (None then use screen overlay)
                bs-modal
                    title {string=}: dialog
                    type {BsDialogType=}: the type of dialog (ie the colour)
                    size {BsDialogSize=}: the size of the dialog

                delay {int=}: number of milliseconds to wait before execute the commands ie redirect/refresh

        :param message: the text or html to be display
        :type display_method: Ajx.DisplayMethod|str
        :param display_method:  the display method
        :type command: Ajx.Command|str
        :param command: the command type
        :type status: Ajx.Status|str
        :param status:  the status
        :param js_on_pre_parse:    the javascript function to be executed before
                                    the AjaxCommand is parsed. If the function return "false" the package
                                    will be ignored.
        :param js_on_post_parse:   the javascript function to be executed after the AjaxCommand is parsed.
                                    Only run after delay is satisfied, and no refresh nor redirect.

        :param js_on_ajax_success:   the javascript function to be executed after the ajax event return successfully
                                    ie ajax-refresh, ajax-get and ajax-post.
        :return:    HttpResponse Json Object
        """
        cmd = OrderedDict([
            ('isAjaxCommand', True,),
            ('message', message,),
            ('displayMethod', display_method,),
            ('command', command,),
            ('status', status,),
        ])

        if js_on_pre_parse:
            cmd['onPreParse'] = js_on_pre_parse

        if js_on_post_parse:
            cmd['onPostParse'] = js_on_post_parse

        if js_on_ajax_success:
            cmd['onAjaxSuccess'] = js_on_ajax_success

        default_options = {
        }

        if status == Ajx.Status.error:
            default_options['title'] = _('Error')

        default_options.update(options)
        return Ajx._return_command(cmd, options)

    @classmethod
    def _return_command(cls, cmd_dict: dict, options: dict):
        # convert key from redirect_url into redirectUrl
        cmd_dict['options'] = dict((Str.snake_to_camel(k), v) for k, v in options.items())
        return HttpResponse(Json.to_json(cmd_dict))
        # endregion
