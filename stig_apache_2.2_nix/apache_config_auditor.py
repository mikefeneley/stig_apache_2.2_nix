# -*- coding: utf-8 -*-

from apache_logger import ApacheLogger

ROOT = "/"
START_DIRECTORY = "<Directory"
END_DIRECTORY = "</Directory>"


class ApacheConfigAuditor:

    """ApacheConfigAuditor checks the directive_list for all STIG requirements
    that involve single or multiline directives from the main Apache
    configuration file on the server.
    """

    def __init__(self, directive_list=None):
        self.directive_list = directive_list
        self.logger = ApacheLogger()


    def audit_config(self):
        """
        self.ssi_disabled()
        self.http_header_limited()
        self.http_line_limited()
        self.symlinks_disabled()
        self.multiviews_disabled()
        self.indexing_disabled()
        self.http_message_limited()
        self.http_header_limited()
        self.minspareservers_set()
        self.startservers_set()
        self.keepalivetimeout_set()
        self.keepalive_set()
        self.timeout_set()
        self.root_denied()
        self.ports_configured()
        self.maxspareservers_set()
        """
        self.ports_configured()
        
    def ssi_disabled(self):
        """Check SV-32753r1_rule: Requires server side includes be disabled to
        prevent external scripts from being execued.

        Finding ID: V-13733

        Review all uncommented Options statements for the following values:

        +IncludesNoExec
        -IncludesNoExec
        -Includes


        -If these values don’t exist this is a finding.
        -If the value does NOT exist, this is a finding.
        -If all enabled Options statement are set to None this is
         not a finding.
        """

        option_exists = False
        ssi_option_disabled = False
        options_set_none = True
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Options":
                option_exists = True
                options = directive.get_options()
                for option in options:
                    if option != "None":
                        options_set_none = False
                    if option == "+IncludesNoExec":
                        ssi_option_disabled = True
                    elif option == "-IncludesNoExec":
                        ssi_option_disabled = True
                    elif option == "-Includes":
                        ssi_option_disabled = True

        if options_set_none and option_exists:
            disabled = True
        elif ssi_option_disabled:
            disabled = True
        else:
            self.logger.ssi_disabled_errmsg()
            disabled = False
        return disabled

    def http_header_field_limited(self):
        """Check SV-32766r2_rule: HTTP request header field size must be limited to
        prevent buffer overflow attacks.

        Finding ID: V-13738

        Check active configuation file for directive:

        LimitRequestFiledSize

        -If no LimitRequestFieldSize directives exist, this is a Finding.
        -If the value of LimitRequestFieldSize is not set to 8190,
         this is a finding. SOMEHOW THIS IS NOT BEING CALLED CORRECTLY
        """

        directive_exists = False
        correct_value = False

        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "LimitRequestFieldSize":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if option == "8190":
                        correct_value = True

        if(directive_exists and correct_value):
            limited = True
        else:
            self.logger.http_header_limited_errmsg()
            limited = False
        return limited


    def http_line_limited(self):
        """Check SV-32768r2_rule: HTTP request line must be limited to
        prevent buffer overflow attacks.

        Finding ID: V-13739

        Check active configuation file for directive:

        LimitRequestLine

        -If no LimitRequestLine directives exist, this is a Finding.
        -If the value of LimitRequestLine is not set to 8190,
         this is a finding.
        """
        directive_exists = False
        correct_value = False

        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "LimitRequestLine":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if option == "8190":
                        correct_value = True
        if(directive_exists and correct_value):
            limited = True
        else:
            self.logger.http_line_limited_errmsg()
            limited = False
        return limited

    def maxclients_set(self):
        """Check SV-36649r2_rule: The maximum number of clients for the server
        must be specified to mitigate ddos attacks.

        Finding ID: V-13730

        Check active configuation file for directive:

        MaxClients

        - If the value of MaxClients is not less than or equal to 256,
          this is a finding.
        - If the directive does not exist, this is NOT a finding
          because it will default to 256."""
        directive_exists = False
        correct_value = False

        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "MaxClients":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if(int(option) < 256):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            correct = False
        return correct

    def symlinks_disabled(self):
        """Check SV-40129r1_rule: The "–FollowSymLinks” setting must be disabled.

        Finding ID: V-13732

        Review all uncommented Options statements for the following values:

        -FollowSymLinks

        - If the value does NOT exist, this is a finding.
        - If all enabled Options statement are set to None
          this is not a finding.
        """
        
        option_exists = False
        symlinks_option_disabled = False
        options_set_none = True
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Options":
                option_exists = True
                options = directive.get_options()
                for option in options:
                    if option != "None":
                        options_set_none = False
                    if option == "-FollowSymLinks":
                        symlinks_option_disabled = True

        if options_set_none and option_exists:
            disabled = True
        elif symlinks_option_disabled:
            disabled = True
        else:
            self.logger.ssi_disabled_errmsg()
            disabled = False
        return disabled

    def multiviews_disabled(self):
        """Check SV-32754r1_rule: The MultiViews directive must be disabled.

        Finding ID: V-13734

        Review all uncommented Options statements for the following value:

        -MultiViews

        - If the value is found on the Options statement, and it does not
          have a preceding ‘-‘, this is a finding.
        - If the value does NOT exist, this is a finding.
        - If all enabled Options statement are set to None
          this is not a finding.
        """
        option_exists = False
        multiviews_option_disabled = False
        options_set_none = True
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Options":
                option_exists = True
                options = directive.get_options()
                for option in options:
                    if option != "None":
                        options_set_none = False
                    if option == "-Multiview":
                        multiviews_option_disabled = True

        if option_exists and options_set_none:
            disabled = True
        elif multiviews_option_disabled:
            disabled = True
        else:
            self.logger.multiviews_disabled_errmsg()
            disabled = False
        return disabled

    def indexing_disabled(self):
        """Check SV-32755r1_rule: Directory indexing must be disabled on
        directories not containing index files.

        Finding ID: V-13735

        Review all uncommented Options statements for the following value:

        -Indexes

        - The value is found on the Options statement, and it does not have a
          preceding ‘-‘, this is a finding.
        - If the value does NOT exist, this is a finding.
        - If all enabled Options statement are set to None
          this is not a finding.
        """

        option_exists = False
        indexing_option_disabled = False
        options_set_none = True
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Options":
                option_exists = True
                options = directive.get_options()
                for option in options:
                    if option != "None":
                        options_set_none = False
                    if option == "-Indexes":
                        indexing_option_disabled = True

        if option_exists and options_set_none:
            disabled = True
        elif indexing_option_disabled:
            disabled = True
        else:
            self.logger.indexing_disabled_errmsg()
            disabled = False
        return disabled

    def http_message_limited(self):
        """Check SV-32756r1_rule: The HTTP request message body size must be limited.

        Finding ID: V-13736

        Check active configuation file for directive:

        LimitRequestBody

        - If the value of LimitRequestBody is not set to 1 or greater or
          does not exist, this is a finding.
        """
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "LimitRequestBody":
                options = directive.get_options()
                for option in options:
                    if(int(option) >= 1):
                        correct_value = True
        if(correct_value):
            limited = True
        else:
            self.logger.http_message_limited_errmsg()
            limited = False
        return limited

    def http_header_limited(self):
        """Check SV-32757r1_rule: The HTTP request header fields must be limited.

        Finding ID: V-13737

        Check active configuation file for directive:

        LimitRequestFields

        - If the value of LimitRequestFields is not set to a value
          greater than 0, this is a finding.
        """

        correct_value = False
        for directive in self.directive_list:
                directive_start = directive.get_directive()
                if directive_start == "LimitRequestFields":
                    options = directive.get_options()
                    for option in options:
                        if(int(option) >= 1):
                            correct_value = True
        if(correct_value):
            limited = True
        else:
            self.logger.http_message_limited_errmsg()
            limited = False
        return limited

    def minspareservers_set(self):
        """Check SV-36646r2_rule: The httpd.conf MinSpareServers
        directive must be set properly.

        Finding ID: V-13728

        Check active configuation file for directive:

        MinSpareServers

        The value needs to be between 5 and 10

        - If the directive is set improperly, this is a finding.
        - If the directive does not exist, this is NOT a finding
          because it will default to 5.
        """

        directive_exists = False
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "MinSpareServers":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if(int(option) >= 5 and int(option) <= 10):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            self.logger.minspareservers_set_errmsg()
            correct = False
        return correct

    def startservers_set(self):
        """Check SV-36645r2_rule: The httpd.conf StartServers
        directive must be set properly.

        Finding ID: V-13727

        Check active configuation file for directive:

        StartServers

        The value needs to be between 5 and 10

        - If the directive is set improperly, this is a finding.
        - If the directive does not exist, this is NOT a finding
          because it will default to 5.
        """

        directive_exists = False
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "StartServers":
                directive_exists = True
                options = directive.get_options()

                for option in options:
                    if(int(option) >= 5 and int(option) <= 10):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            self.logger.startservers_set_errmsg()
            correct = False
        return correct

    def keepalivetimeout_set(self):
        """Check SV-32877r1_rule: The KeepAliveTimeout directive must be defined.

        Finding ID: V-13726

        Check active configuation file for directive:

        KeepAliveTimeout

        The value needs to be less than or equal to 15

        - If the directive is set improperly, this is a finding.
        - If the directive does not exist, this is NOT a finding
          because it will default to 5.
        """

        directive_exists = False
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "KeepAliveTimeout":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if(int(option) <= 15):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            correct = False
        return correct

    def keepalive_set(self):
        """Check SV-32844r2_rule: The KeepAliveTimeout directive
        must be defined.

        Finding ID: V-13725

        Check active configuation file for directive:

        KeepAlive

        - Verify the Value of KeepAlive is set to On, If not, it is a finding
        """

        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "KeepAlive":
                options = directive.get_options()
                for option in options:
                    if(option == "On"):
                        correct_value = True
        if(correct_value):
            correct = True
        else:
            correct = False
        return correct

    def timeout_set(self):
        """Check SV-32977r1_rule: The Timeout directive must be properly set.

        Finding ID: V-13724

        Check active configuation file for directive:

        Timeout

        - Verify the value is 300 or less if not, this is a finding.
        - If the directive does not exist, this is not a finding
          because it will default to 300
        """
        directive_exists = False
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Timeout":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if(int(option) <= 300):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            correct = False
        return correct

    def maxspareservers_set(self):
        """Check SV-36648r2_rule: The MaxSpareServers directive must be set properly.

        Finding ID: V-13729

        Check active configuation file for directive:

        MaxSpareServers

        - The value needs to be 10 or less
        - If the directive is set improperly, this is a finding."""
        directive_exists = False
        correct_value = False
        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "MaxSpareServers":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    if(int(option) <= 10):
                        correct_value = True
        if(correct_value or not directive_exists):
            correct = True
        else:
            correct = False
        return correct


    def ports_configured(self):
        """Check SV-33228r1_rule: The web server must be configured to
        listen on a specific IP address and port.

        Finding ID: V-26326
        """
        directive_exists = False

        for directive in self.directive_list:
            directive_start = directive.get_directive()
            if directive_start == "Listen":
                directive_exists = True
                options = directive.get_options()
                for option in options:
                    valid_address = is_valid_address(option)
                    if(not valid_address):
                        return False

        if(not directive_exists):
            return False
        else:
            return True


    def is_valid_address(self, address):
        """ Check for the criteria which would cause the ports/ip 
        configuartion to be a finding. Very rough checking criteria.
        Need better way to verify conditions...
        """
        valid_address = True
        if "0.0.0.0" in address:    # Check all zero ip address
            valid_address = False
        if("]" in address and "]:" not in address): # ipv6 with no port
            valid_address = False
        if("[" not in valid address and ":" not in address): # ipv4 no port
            valid_address = False

        return valid_address



    def root_denied(self):
        """Check SV-33232r1_rule: The ability to override the access
        configuration for the OS root directory must be disabled.

        Finding ID: V-26393

        For every root directory entry ensure the following entry exists:

        AllowOverride None

        - If the statement above is not found in the root directory
          statement, this is a finding.
        - If Allow directives are included in the root directory
          statement, this is a finding.
          DO THIS BETTER
        """

        root_exists = False
        option_exists = False
        option_correct = False

        i = 0
        while i < len(self.directive_list):
            directive = self.directive_list[i]
            directive_start = directive.get_directive()

            if(directive_start == START_DIRECTORY):
                tmp = i
                directory_list = self.get_directory_list(tmp)

                first_directive = directory_list[0]
                directive_info = first_directive[0]
                directory = first_directive[1]
                if(directory == '/'):
                    for line in directory_list:
                        directive_info = line[0]
                        directive = directive_info.get_directive()
                        options = directive_info.get_options()
                        print(directive)
                        if(directive == 'AllowOverride'):
                            option_exists = True
                            if(options[0] == "None"):
                                option_correct = True
            i += 1

        return option_exists and option_correct and root_exists



    def get_directory_list(self, current_index):
        directory_options = []

        i = current_index + 1
        directive_info = self.directive_list[current_index]
        directory = self.get_directory(directive_info)
        while True:
            directive_info = self.directive_list[i]
            if self.check_end_directory(directive_info):
                break
            directory_options.append((directive_info, directory))
            i += 1
        return directory_options

    def get_directory(self, directive_info):
        options = directive_info.get_options()
        directory = options[0].split(">")
        return directory[0]

    def check_end_directory(self, directive_info):
        directive = directive_info.get_directive()
        if directive == END_DIRECTORY:
            return True
        else:
            return False

