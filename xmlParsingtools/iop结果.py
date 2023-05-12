# {遍历标签序号：{标签名称：{标签序号：[{标签所有的属性},{遍历标签下的标签},{标签中的内容}]}}}

dock = {0: {'site': {0: [{'average_response_time': '1343', 'average_send_count': '7', 'domain': 'iop.cicconline.com',
                          'failed_request_count': '1254', 'issuecnt': '6', 'name': 'asset_0806/iop.cicconline.com:443',
                          'receive_bytes': '197722916', 'recent_failed_request_count': '0', 'request_count': '27610',
                          'scan_time': '3609', 'scan_time_remain': '0', 'score': '82', 'send_bytes': '15034836',
                          'server': 'nginx/1.18.0', 'site_port': '443', 'site_progress': '100',
                          'site_protocol': 'https', 'start_first_time': '1659734088', 'start_time': '0',
                          'test_count': '42471', 'test_done_count': '42471', 'time': '1659734096', 'url_count': '143',
                          'visited_count': '143'},
                         {0: {'issuetype': {
                             0: [{
                                 'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]基本上，cookie的唯一必需属性是“name”字段，建议设置“secure”属性，以保证cookie的安全。 </pre> </html>',
                                 'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>配置不当<br/> <b>弱点描述：</b><br/> 在应用程序测试过程中，检测到所测试的Web应用程序设置了不含“secure”属性的会话cookie。由于此会话cookie不包含“secure”属性，所以用户可以通过未加密的http协议传输Cookie,可能造成用户信息被窃听。</pre>  ',
                                 'level': '低危',
                                 'name': '会话Cookie中缺少secure属性'}, {
                                 0: {'issuedata': {0: [
                                     {'issue': 'cookie_without_secure',
                                      'url': 'https://iop.cicconline.com/',
                                      'value': 'https://iop.cicconline.com/'},
                                     None, None]}}}, '\n        '], 1: [{
                                 'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b>  [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] .  <b>开发语言的建议：</b><br/><pre> [1] 检查全局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。 ',
                                 'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> 在Web应用程序与数据库交互过程中，如果Web应用程序传递供数据库查询的数据不符合数据库语法，或者Web应用查询程序本身存在相关语法错误，这样会将数据库错误结果直接反馈给访问者。 </pre> ',
                                 'level': '低危',
                                 'name': '数据库错误'},
                                 {
                                     1: {
                                         'issuedata': {
                                             0: [
                                                 {
                                                     'issue': 'db_error',
                                                     'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                                     'value': 'ORA-0175'},
                                                 None,
                                                 None]}}},
                                 None],
                             2: [{
                                 'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]尽量在站点页面上显示最少的email地址。 [2]培养良好的安全意识。',
                                 'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> Web应用程序中错误消息或者代码中可能含有email地址，作为站点人员的联系信息。 攻击者可能利用这些联系信息，通过搜索引擎等社会工程学手段进行攻击。',
                                 'level': '信息', 'name': 'E-Mail地址'}, {
                                 2: {'issuedata': {
                                     0: [
                                         {'issue': 'email_address',
                                          'url': 'https://iop.cicconline.com/IOPWeb/assets/javascripts/lib/jqGrid/js/trirand/jquery.jqGrid.min.js?v=1.0.1',
                                          'value': 'tony@trirand.com '}, None,
                                         None]}}}, None],
                             3: [{
                                 'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> 解决SQL注入问题的关键是对所有可能来自用户输入的数据进行严格的检查、对数据库配置使用最小权限原则。<br/> <p> [1]所有的查询语句都使用数据库提供的参数化查询接口，参数化的语句使用参数而不是将用户输入变量嵌入到SQL语句中。当前几乎所有的数据库系统都提供了参数化SQL语句执行接口，使用此接口可以非常有效的防止SQL注入攻击。</p> [2]对进入数据库的特殊字符（\'"\\尖括号&*;等）进行转义处理，或编码转换。</p> [3]严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型。</p> [4]数据长度应该严格规定，能在一定程度上防止比较长的SQL注入语句无法正确执行。</p> [5]网站每个数据层的编码统一，建议全部使用UTF-8编码，上下层编码不一致有可能导致一些过滤模型被绕过。</p> [6]严格限制网站用户的数据库的操作权限，给此用户提供仅仅能够满足其工作的权限，从而最大限度的减少注入攻击对数据库的危害。</p> [7]避免网站显示SQL错误信息，比如类型错误、字段不匹配等，防止攻击者利用这些错误信息进行一些判断。</p> [8]确认PHP配置文件中的magicquotesgpc选项保持开启。</p> [9]在部署你的应用前，始终要做安全审评(security review)。建立一个正式的安全过程(formal security process)，在每次你做更新时，对所有的编码做审评。后面一点特别重要。不论是发布部署应用还是更新应用，请始终坚持做安全审评。</p> [10]千万别把敏感性数据在数据库里以明文存放。</p> [11]使用第三方Web防火墙来加固整个网站系统。</p><br/> 应用程序级别的漏洞，仅仅依靠对服务器的基本设置做一些改动是不能够解决的，必须从提高应用程序的开发人员的安全意识入手，加强对代码安全性的控制，在服务端正式处理之前对每个被提交的参数进行合法性检查，以从根本上解决注入问题。 </body> </html>',
                                 'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>SQL注入<br/> <b>弱点描述：</b><br/> SQL注入（SQL Injection）技术在国外最早出现在1999年，我国在2002年后开始大量出现。SQL注入攻击，SQL注入是针对一种数据库而言的，而不是针对网页语言。在任何使用了数据库查询环境下都可能存在，简单来说就是从一个数据库获得未经授权的访问和直接检索。  造成SQL注入攻击漏洞的原因，是由于程序在编写Web程序时，没有对浏览器端提交的参数进行严格的过滤和判断。用户可以修改构造参数，提交SQL查询语句，并传递至服务端，从而获取想要的敏感信息，甚至执行危险的代码或系统命令。  SQL注入攻击包括通过输入数据从客户端插入或“注入”SQL查询到应用程序。一个成功的SQL注入攻击可以从数据库中获取敏感数据、修改数据库数据（插入/更新/删除） 、执行数据库管理操作</b></pre>  <br/><b>主要危害：</b><br/> [1]未经授权状况下操作数据库中的数据。 [2]恶意篡改网页内容。 [3]私自添加系统帐号或者是数据库使用者帐号。 [4]网页挂马。 [5]与其它漏洞结合，修改系统设置，查看系统文件，执行系统命令等。</pre>  <br/><b>参考链接：</b><br/> [1]<a href="http://baike.baidu.com/view/3896.htm?fr=ala0" target="_blank">http://baike.baidu.com/view/3896.htm?fr=ala0</a>',
                                 'level': '紧急',
                                 'name': 'SQL错误信息注入'},
                                 {3: {
                                     'issuedata': {
                                         0: [{
                                             'issue': 'error_sql_injection',
                                             'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                             'value': '参数: taAccountId=, 注入类型: 字符型, 数据库类型: Oracle,数据库名: IMSP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus ,用户名: NAVAPP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus '},
                                             None,
                                             None]}}},
                                 None], 4: [{
                                 'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b> <pre> [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] . </pre> <b>开发语言的建议:</b> <pre> [1] 检查入局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。  </pre> </body> </html>',
                                 'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/>Web应用程序在处理访问者的请求时，如果符合Web应用程序的逻辑或者Web应用程序本身没有异常，那么将结果直接反馈给访问者。如果提交不符合Web应用程序逻辑的数据，Web应用程序在处理这些请求的时候未做相应的处理，直接把Web服务器的错误反馈给访问者。',
                                 'level': '低危',
                                 'name': 'Web应用程序错误'},
                                 {4: {
                                     'issuedata': {
                                         0: [
                                             {
                                                 'issue': 'web_application_error',
                                                 'url': 'https://iop.cicconline.com/IOPWeb/login?locale=zh_CN',
                                                 'value': '500 Internal Server Error'},
                                             None,
                                             None],
                                         1: [
                                             {
                                                 'issue': 'web_application_error',
                                                 'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                                 'value': '500 Internal Server Error'},
                                             None,
                                             None]}}},
                                 None]}}},
                         '\n        ']}}}
c = {'site': {0: [{'average_response_time': '1343', 'average_send_count': '7', 'domain': 'iop.cicconline.com',
                   'failed_request_count': '1254', 'issuecnt': '6', 'name': 'asset_0806/iop.cicconline.com:443',
                   'receive_bytes': '197722916', 'recent_failed_request_count': '0', 'request_count': '27610',
                   'scan_time': '3609', 'scan_time_remain': '0', 'score': '82', 'send_bytes': '15034836',
                   'server': 'nginx/1.18.0', 'site_port': '443', 'site_progress': '100', 'site_protocol': 'https',
                   'start_first_time': '1659734088', 'start_time': '0', 'test_count': '42471',
                   'test_done_count': '42471', 'time': '1659734096', 'url_count': '143', 'visited_count': '143'}, {
                      'issuetype': {
                          0: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]基本上，cookie的唯一必需属性是“name”字段，建议设置“secure”属性，以保证cookie的安全。 </pre> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>配置不当<br/> <b>弱点描述：</b><br/> 在应用程序测试过程中，检测到所测试的Web应用程序设置了不含“secure”属性的会话cookie。由于此会话cookie不包含“secure”属性，所以用户可以通过未加密的http协议传输Cookie,可能造成用户信息被窃听。</pre>  ',
                              'level': '低危', 'name': '会话Cookie中缺少secure属性'}, {
                              'issuedata': {
                                  0: [
                                      {'issue': 'cookie_without_secure', 'url': 'https://iop.cicconline.com/',
                                       'value': 'https://iop.cicconline.com/'}, None, None]}}, '\n        '],
                          1: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b>  [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] .  <b>开发语言的建议：</b><br/><pre> [1] 检查全局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。 ',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> 在Web应用程序与数据库交互过程中，如果Web应用程序传递供数据库查询的数据不符合数据库语法，或者Web应用查询程序本身存在相关语法错误，这样会将数据库错误结果直接反馈给访问者。 </pre> ',
                              'level': '低危',
                              'name': '数据库错误'},
                              {'issuedata': {
                                  0: [{
                                      'issue': 'db_error',
                                      'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                      'value': 'ORA-0175'},
                                      None,
                                      None]}},
                              None],
                          2: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]尽量在站点页面上显示最少的email地址。 [2]培养良好的安全意识。',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> Web应用程序中错误消息或者代码中可能含有email地址，作为站点人员的联系信息。 攻击者可能利用这些联系信息，通过搜索引擎等社会工程学手段进行攻击。',
                              'level': '信息',
                              'name': 'E-Mail地址'},
                              {'issuedata': {
                                  0: [
                                      {
                                          'issue': 'email_address',
                                          'url': 'https://iop.cicconline.com/IOPWeb/assets/javascripts/lib/jqGrid/js/trirand/jquery.jqGrid.min.js?v=1.0.1',
                                          'value': 'tony@trirand.com '},
                                      None,
                                      None]}},
                              None],
                          3: [{
                              'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> 解决SQL注入问题的关键是对所有可能来自用户输入的数据进行严格的检查、对数据库配置使用最小权限原则。<br/> <p> [1]所有的查询语句都使用数据库提供的参数化查询接口，参数化的语句使用参数而不是将用户输入变量嵌入到SQL语句中。当前几乎所有的数据库系统都提供了参数化SQL语句执行接口，使用此接口可以非常有效的防止SQL注入攻击。</p> [2]对进入数据库的特殊字符（\'"\\尖括号&*;等）进行转义处理，或编码转换。</p> [3]严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型。</p> [4]数据长度应该严格规定，能在一定程度上防止比较长的SQL注入语句无法正确执行。</p> [5]网站每个数据层的编码统一，建议全部使用UTF-8编码，上下层编码不一致有可能导致一些过滤模型被绕过。</p> [6]严格限制网站用户的数据库的操作权限，给此用户提供仅仅能够满足其工作的权限，从而最大限度的减少注入攻击对数据库的危害。</p> [7]避免网站显示SQL错误信息，比如类型错误、字段不匹配等，防止攻击者利用这些错误信息进行一些判断。</p> [8]确认PHP配置文件中的magicquotesgpc选项保持开启。</p> [9]在部署你的应用前，始终要做安全审评(security review)。建立一个正式的安全过程(formal security process)，在每次你做更新时，对所有的编码做审评。后面一点特别重要。不论是发布部署应用还是更新应用，请始终坚持做安全审评。</p> [10]千万别把敏感性数据在数据库里以明文存放。</p> [11]使用第三方Web防火墙来加固整个网站系统。</p><br/> 应用程序级别的漏洞，仅仅依靠对服务器的基本设置做一些改动是不能够解决的，必须从提高应用程序的开发人员的安全意识入手，加强对代码安全性的控制，在服务端正式处理之前对每个被提交的参数进行合法性检查，以从根本上解决注入问题。 </body> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>SQL注入<br/> <b>弱点描述：</b><br/> SQL注入（SQL Injection）技术在国外最早出现在1999年，我国在2002年后开始大量出现。SQL注入攻击，SQL注入是针对一种数据库而言的，而不是针对网页语言。在任何使用了数据库查询环境下都可能存在，简单来说就是从一个数据库获得未经授权的访问和直接检索。  造成SQL注入攻击漏洞的原因，是由于程序在编写Web程序时，没有对浏览器端提交的参数进行严格的过滤和判断。用户可以修改构造参数，提交SQL查询语句，并传递至服务端，从而获取想要的敏感信息，甚至执行危险的代码或系统命令。  SQL注入攻击包括通过输入数据从客户端插入或“注入”SQL查询到应用程序。一个成功的SQL注入攻击可以从数据库中获取敏感数据、修改数据库数据（插入/更新/删除） 、执行数据库管理操作</b></pre>  <br/><b>主要危害：</b><br/> [1]未经授权状况下操作数据库中的数据。 [2]恶意篡改网页内容。 [3]私自添加系统帐号或者是数据库使用者帐号。 [4]网页挂马。 [5]与其它漏洞结合，修改系统设置，查看系统文件，执行系统命令等。</pre>  <br/><b>参考链接：</b><br/> [1]<a href="http://baike.baidu.com/view/3896.htm?fr=ala0" target="_blank">http://baike.baidu.com/view/3896.htm?fr=ala0</a>',
                              'level': '紧急', 'name': 'SQL错误信息注入'}, {'issuedata': {0: [
                              {'issue': 'error_sql_injection',
                               'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                               'value': '参数: taAccountId=, 注入类型: 字符型, 数据库类型: Oracle,数据库名: IMSP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus ,用户名: NAVAPP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus '},
                              None, None]}}, None],
                          4: [{
                              'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b> <pre> [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] . </pre> <b>开发语言的建议:</b> <pre> [1] 检查入局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。  </pre> </body> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/>Web应用程序在处理访问者的请求时，如果符合Web应用程序的逻辑或者Web应用程序本身没有异常，那么将结果直接反馈给访问者。如果提交不符合Web应用程序逻辑的数据，Web应用程序在处理这些请求的时候未做相应的处理，直接把Web服务器的错误反馈给访问者。',
                              'level': '低危', 'name': 'Web应用程序错误'}, {
                              'issuedata': {
                                  0: [
                                      {'issue': 'web_application_error',
                                       'url': 'https://iop.cicconline.com/IOPWeb/login?locale=zh_CN',
                                       'value': '500 Internal Server Error'}, None,
                                      None],
                                  1: [{'issue': 'web_application_error',
                                       'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                       'value': '500 Internal Server Error'},
                                      None, None]}}, None]}},
                  '\n        ']}}

d = {'site': {0: [{'average_response_time': '1343', 'average_send_count': '7', 'domain': 'iop.cicconline.com',
                   'failed_request_count': '1254', 'issuecnt': '6', 'name': 'asset_0806/iop.cicconline.com:443',
                   'receive_bytes': '197722916', 'recent_failed_request_count': '0', 'request_count': '27610',
                   'scan_time': '3609', 'scan_time_remain': '0', 'score': '82', 'send_bytes': '15034836',
                   'server': 'nginx/1.18.0', 'site_port': '443', 'site_progress': '100', 'site_protocol': 'https',
                   'start_first_time': '1659734088', 'start_time': '0', 'test_count': '42471',
                   'test_done_count': '42471', 'time': '1659734096', 'url_count': '143', 'visited_count': '143'}, {
                      'issuetype': {
                          0: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]基本上，cookie的唯一必需属性是“name”字段，建议设置“secure”属性，以保证cookie的安全。 </pre> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>配置不当<br/> <b>弱点描述：</b><br/> 在应用程序测试过程中，检测到所测试的Web应用程序设置了不含“secure”属性的会话cookie。由于此会话cookie不包含“secure”属性，所以用户可以通过未加密的http协议传输Cookie,可能造成用户信息被窃听。</pre>  ',
                              'level': '低危', 'name': '会话Cookie中缺少secure属性'},
                              {'issuedata': {0: [
                                  {'issue': 'cookie_without_secure', 'url': 'https://iop.cicconline.com/',
                                   'value': 'https://iop.cicconline.com/'}, None, None]}}, '\n        '],
                          1: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b>  [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] .  <b>开发语言的建议：</b><br/><pre> [1] 检查全局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。 ',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> 在Web应用程序与数据库交互过程中，如果Web应用程序传递供数据库查询的数据不符合数据库语法，或者Web应用查询程序本身存在相关语法错误，这样会将数据库错误结果直接反馈给访问者。 </pre> ',
                              'level': '低危',
                              'name': '数据库错误'},
                              {'issuedata': {0: [
                                  {'issue': 'db_error',
                                   'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                   'value': 'ORA-0175'},
                                  None,
                                  None]}},
                              None],
                          2: [{
                              'advice': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> [1]尽量在站点页面上显示最少的email地址。 [2]培养良好的安全意识。',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/> Web应用程序中错误消息或者代码中可能含有email地址，作为站点人员的联系信息。 攻击者可能利用这些联系信息，通过搜索引擎等社会工程学手段进行攻击。',
                              'level': '信息',
                              'name': 'E-Mail地址'},
                              {
                                  'issuedata': {
                                      0: [
                                          {
                                              'issue': 'email_address',
                                              'url': 'https://iop.cicconline.com/IOPWeb/assets/javascripts/lib/jqGrid/js/trirand/jquery.jqGrid.min.js?v=1.0.1',
                                              'value': 'tony@trirand.com '},
                                          None,
                                          None]}},
                              None],
                          3: [{
                              'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> 解决SQL注入问题的关键是对所有可能来自用户输入的数据进行严格的检查、对数据库配置使用最小权限原则。<br/> <p> [1]所有的查询语句都使用数据库提供的参数化查询接口，参数化的语句使用参数而不是将用户输入变量嵌入到SQL语句中。当前几乎所有的数据库系统都提供了参数化SQL语句执行接口，使用此接口可以非常有效的防止SQL注入攻击。</p> [2]对进入数据库的特殊字符（\'"\\尖括号&*;等）进行转义处理，或编码转换。</p> [3]严格限制变量类型，比如整型变量就采用intval()函数过滤，数据库中的存储字段必须对应为int型。</p> [4]数据长度应该严格规定，能在一定程度上防止比较长的SQL注入语句无法正确执行。</p> [5]网站每个数据层的编码统一，建议全部使用UTF-8编码，上下层编码不一致有可能导致一些过滤模型被绕过。</p> [6]严格限制网站用户的数据库的操作权限，给此用户提供仅仅能够满足其工作的权限，从而最大限度的减少注入攻击对数据库的危害。</p> [7]避免网站显示SQL错误信息，比如类型错误、字段不匹配等，防止攻击者利用这些错误信息进行一些判断。</p> [8]确认PHP配置文件中的magicquotesgpc选项保持开启。</p> [9]在部署你的应用前，始终要做安全审评(security review)。建立一个正式的安全过程(formal security process)，在每次你做更新时，对所有的编码做审评。后面一点特别重要。不论是发布部署应用还是更新应用，请始终坚持做安全审评。</p> [10]千万别把敏感性数据在数据库里以明文存放。</p> [11]使用第三方Web防火墙来加固整个网站系统。</p><br/> 应用程序级别的漏洞，仅仅依靠对服务器的基本设置做一些改动是不能够解决的，必须从提高应用程序的开发人员的安全意识入手，加强对代码安全性的控制，在服务端正式处理之前对每个被提交的参数进行合法性检查，以从根本上解决注入问题。 </body> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>SQL注入<br/> <b>弱点描述：</b><br/> SQL注入（SQL Injection）技术在国外最早出现在1999年，我国在2002年后开始大量出现。SQL注入攻击，SQL注入是针对一种数据库而言的，而不是针对网页语言。在任何使用了数据库查询环境下都可能存在，简单来说就是从一个数据库获得未经授权的访问和直接检索。  造成SQL注入攻击漏洞的原因，是由于程序在编写Web程序时，没有对浏览器端提交的参数进行严格的过滤和判断。用户可以修改构造参数，提交SQL查询语句，并传递至服务端，从而获取想要的敏感信息，甚至执行危险的代码或系统命令。  SQL注入攻击包括通过输入数据从客户端插入或“注入”SQL查询到应用程序。一个成功的SQL注入攻击可以从数据库中获取敏感数据、修改数据库数据（插入/更新/删除） 、执行数据库管理操作</b></pre>  <br/><b>主要危害：</b><br/> [1]未经授权状况下操作数据库中的数据。 [2]恶意篡改网页内容。 [3]私自添加系统帐号或者是数据库使用者帐号。 [4]网页挂马。 [5]与其它漏洞结合，修改系统设置，查看系统文件，执行系统命令等。</pre>  <br/><b>参考链接：</b><br/> [1]<a href="http://baike.baidu.com/view/3896.htm?fr=ala0" target="_blank">http://baike.baidu.com/view/3896.htm?fr=ala0</a>',
                              'level': '紧急', 'name': 'SQL错误信息注入'}, {'issuedata': {0: [
                              {'issue': 'error_sql_injection',
                               'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                               'value': '参数: taAccountId=, 注入类型: 字符型, 数据库类型: Oracle,数据库名: IMSP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus ,用户名: NAVAPP does not exist ORA-06512: at &quot;CTXSYS.DRUE&quot;, line 160 ORA-06512: at &quot;CTXSYS.DRITHSX&quot;, line 540 ORA-06512: at line 1   org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:978)  org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:857)  javax.servlet.http.HttpServlet.service(HttpServlet.java:622)  org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:842)  javax.servlet.http.HttpServlet.service(HttpServlet.java:729)  org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)  org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:61)  org.apache.shiro.web.servlet.AdviceFilter.executeChain(AdviceFilter.java:108)  org.apache.shiro.web.servlet.AdviceFilter.doFilterInternal(AdviceFilter.java:137)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.apache.shiro.web.servlet.ProxiedFilterChain.doFilter(ProxiedFilterChain.java:66)  org.apache.shiro.web.servlet.AbstractShiroFilter.executeChain(AbstractShiroFilter.java:449)  org.apache.shiro.web.servlet.AbstractShiroFilter$1.call(AbstractShiroFilter.java:365)  org.apache.shiro.subject.support.SubjectCallable.doCall(SubjectCallable.java:90)  org.apache.shiro.subject.support.SubjectCallable.call(SubjectCallable.java:83)  org.apache.shiro.subject.support.DelegatingSubject.execute(DelegatingSubject.java:387)  org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:362)  org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)  org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:344)  org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:261)  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:85)  org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) </pre><p><b>Root Cause</b></p><pre>java.lang.Exception: java.sql.SQLException: ORA-20000: Oracle Text error: DRG-11701: thesaurus '},
                              None, None]}}, None],
                          4: [{
                              'advice': '<html> <body> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%"> <b>一般性的建议：</b><br/><pre> <b>过滤客户端提交的危险字符，客户端提交方式包含GET、POST、COOKIE、User-Agent、Referer、Accept-Language等，其中危险字符如下：</b> <pre> [1] | [2] & [3] ; [4] $ [5] % [6] @ [7] \' [8] " [9] <> [10] () [11] + [12] CR [13] LF [14] , [15] . </pre> <b>开发语言的建议:</b> <pre> [1] 检查入局请求，以了解所有预期的参数和值是否存在。 当参数缺失时，发出适当的错误消息，或使用缺省值。 [2] 应用程序应验证其输入是否由有效字符组成（解码后）。 例如，应拒绝包含空字节（编码为 %00）、单引号、引号等的输入值。 [3] 确保值符合预期范围和类型。 如果应用程序预期特定参数具有特定集合中的值，那么该应用程序应确保其接收的值确实属于该集合。 例如，如果应用程序预期值在 10..99 范围内，那么就该确保该值确实是数字，且在 10..99 范围内。 [4] 验证数据属于提供给客户端的集合。 [5] 请勿在生产环境中输出调试错误消息和异常。  </pre> </body> </html>',
                              'desc': '<html> <div style="word-wrap: break-word;word-break:break-all;font-size: 12px;LINE-HEIGHT: 150%">     <pre> <b>漏洞类型：</b>信息泄漏<br/> <b>弱点描述：</b><br/>Web应用程序在处理访问者的请求时，如果符合Web应用程序的逻辑或者Web应用程序本身没有异常，那么将结果直接反馈给访问者。如果提交不符合Web应用程序逻辑的数据，Web应用程序在处理这些请求的时候未做相应的处理，直接把Web服务器的错误反馈给访问者。',
                              'level': '低危', 'name': 'Web应用程序错误'}, {
                              'issuedata': {
                                  0: [
                                      {'issue': 'web_application_error',
                                       'url': 'https://iop.cicconline.com/IOPWeb/login?locale=zh_CN',
                                       'value': '500 Internal Server Error'},
                                      None, None],
                                  1: [{'issue': 'web_application_error',
                                       'url': 'https://iop.cicconline.com/getLoginAccess?taAccountId=',
                                       'value': '500 Internal Server Error'},
                                      None, None]}}, None]}},
                  '\n        ']}}
