SULWatcher
==========

**SULWatcher** notifies [`#cvn-unifications`](irc://irc.freenode.net/cvn-unifications) of [account unifications](http://meta.wikimedia.org/wiki/Help:Unified_login).

Commands
--------

You need to be voiced in IRC to be able to use these commands. Note that the commands start with the bot's nickname, whatever it is, plus a
colon. Normally the bot runs using two nicks (SULWatcher and WatcherSUL) &ndash; issuing a command to either one has the same effect. `SULWatcher:` is
used for these examples.
<table class="wikitable" style="font-size:85%">
<tr>
    <th>Command</th>
    <th>Description</th>
    <th> Example</th>
</tr>

<tr>
<td>SULWatcher: test</td>
<td>Test if the bot is alive</td>
<td>SULWatcher: test</td>
</tr>

<tr>
<td>SULWatcher: test <i>[string]</i> regex <i>[regex]</i></td>
<td>Test the regex against the string</td>
<td>SULWatcher: test grawp regex <code>\bpoop\b</code></td>
</tr>

<tr>
<td>SULWatcher: find regex <i>[regex]</i></td>
<td>Find information on a given regex</td>
<td>SULWatcher: find regex <code>\bpoop\b</code></td>
</tr>

<tr>
<td>SULWatcher: find match <i>[string]</i></td>
<td>Find the regex which matches the provided string</td>
<td>SULWatcher: find match <code>\bpoop\b</code></td>
</tr>

<tr>
<td>SULWatcher: find adder <i>[cloak]</i></td>
<td>Find the regexes attributed to a given cloak</td>
<td>SULWatcher: find adder <i>wikimedia/mikelifeguard</i></td>
</tr>

<tr>
<td>SULWatcher: find number <i>[#]</i></td>
<td>Find information on a given entry</td>
<td>SULWatcher: find number 3</td>
</tr>

<tr>
<td>SULWatcher: add reason <i>[#]</i> <i>[reason]</i></td>
<td>Add a reason for a certain entry if it is attributed to you</td>
<td>SULWatcher: add reason 1 suspicious - matches pattern vandalism</td>
</tr>

<tr>
<td>SULWatcher: add reason <i>[#]</i> <b>!</b> <i>[reason]</i></td>
<td>Re-attribute the entry to you with a given reason</td>
<td>SULWatcher: add reason 1 ! I want to take credit for someone else's work</td>
</tr>

<tr>
<td>SULWatcher: (add&#124;remove&#124;list) badword <i>[regex]</i></td>
<td>Add/remove/list regexes to match against unifications</td>
<td>SULWatcher: add badword <code>\bpoop\b</code><br />SULWatcher: list badword</td>
</tr>

<tr>
<td>SULWatcher: (add&#124;remove&#124;list) whitelist <i>[username]</i></td>
<td>Add/remove/list users who are whitelisted</td>
<td>SULWatcher: add whitelist Mike.lifeguard<br />SULWatcher: list whitelist</td>
</tr>

<tr>
<td>SULWatcher: edit <i>[#]</i> enable&nbsp</td>
<td>Re-enable an existing regex</td>
<td>SULWatcher: edit 2 enable</code></td>
</tr>

<tr>
<td>SULWatcher: edit <i>[#]</i> (regex&#124;reason) <i>[whatever]</i></td>
<td>Change the regex/reason for an entry, if it is attributed to you</td>
<td>SULWatcher: edit 2 regex <code>\bpoop\b</code></td>
</tr>

<tr>
<td>SULWatcher: edit <i>[#]</i> (regex&#124;reason) <b>!</b> <i>[whatever]</i></td>
<td>Change the regex/reason for an entry, re-attributing it to you</td>
<td>SULWatcher: edit 2 reason ! Added word boundaries for fewer false positives</td>
</tr>

<tr>
<td>SULWatcher: edit <i>[#]</i> case <i>(true&#124;false)</i></td>
<td>Make an entry either case sensitive or insensitive</td>
<td>SULWatcher: edit 2 case true</td>
</tr>

<tr>
<td align="center" colspan="3" style="font-weight:bold;">For <i>list</i> commands, don't provide a (regex&#124;cloak&#124;nick&#124;username).</td>
</tr>

<tr>
<td align="center" colspan="3"> The following commands are restricted to opped users.</td>
</tr>

<tr>
<th>Restricted command</th>
<th>Description</th>
<th>Example</th>
</tr>

<tr>
<td>SULWatcher: restart</td>
<td>Restart the bots</td>
<td>SULWatcher: restart</td>
</tr>

<tr>
<td>SULWatcher: restart rc</td>
<td>Restart the [RC](http://meta.wikimedia.org/wiki/Help:Recent_changes) reader</td>
<td>SULWatcher: restart rc</td>
</tr>

<tr>
<td>SULWatcher: die</td>
<td>Kill all the bots</td>
<td>SULWatcher: die<span style="color:grey;">*</span>
</td>
</tr>

<tr>
<td align="center" colspan="3" style="color:grey;">*Note that the bot uses <a href="https://wiki.toolserver.org/view/Cron">cron</a> and <a href="https://wiki.toolserver.org/view/Phoenix">phoenix</a> to stay up &ndash; if you kill it, it will come back in <a href="http://toolserver.org/~stewardbots/docs/crontab-linux">about 10 minutes</a>. Use this for a hard restart in case the soft restart above fails.</td>
</tr>
</table>

Reports
-------

[Reports](http://toolserver.org/~stewardbots/SULWatcher/index.php) of SULWatcher's regexes and matches are available for privileged users.

Regex help
----------

If you don't know [regex](http://en.wikipedia.org/wiki/Regex), you can simply enter strings with nothing fancy, and that will work pretty well. Although the bot isn't a wiki, people can still edit - ask for help, or someone will come along behind you and make your rule better by using fancier regex. If you're inclined to learn, here are some starting points:

*   <http://etext.lib.virginia.edu/services/helpsheets/unix/regex.html>
*   <http://codeproject.com/dotnet/RegexTutorial.asp>
*   <http://docs.python.org/howto/regex.html>
