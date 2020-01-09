### Commit Ordering
```
--date-order
  show commits in the commit timestamp order.
--author-date-order
  show commits in the author timestamp order.
--topo-order
For example, in a commit history like this:

                   ---1----2----4----7
                       \              \
                        3----5----6----8---

 where the numbers denote the order of commit timestamps, git
 rev-list and friends with --date-order show the commits in the
 timestamp order: 8 7 6 5 4 3 2 1.
 With --topo-order, they would show 8 6 5 3 7 4 2 1 (or 8 7 4 2 6 5 3 1);
```
### Commit Formatting
```bash
--abbrev-commit
  Instead of showing the full 40-byte hexadecimal commit object name
  show only a partial prefix. Non default number of digits can be specified with "--abbrev=<n>"

--oneline
  This is a shorthand for "--pretty=oneline --abbrev-commit" used together

--encoding=<encoding>
   The commit objects record the encoding used for the log message in their encoding header; defaults to UTF-8.

--show-signature
  Check the validity of a signed commit object by passing the
  signature to gpg --verify and show the output.  

--relative-date
  Synonym for --date=relative.  
--date=(relative|local|default|iso|rfc|short|raw)

--parents
  Print also the parents of the commit object name  
--children
  Print also the children of the commit object name

--graph
  Draw a text-based graphical representation of the commit history on the left hand side of the output.

--pretty[=<format>], --format=<format>
```
### pretty  format
```
#内建格式
oneline
               <sha1> <title line>
short
               commit <sha1>
               Author: <author>
               <title line>
medium
               commit <sha1>
               Author: <author>
               Date:   <author date>
               <title line>
               <full commit message>
full
               commit <sha1>
               Author: <author>
               Commit: <committer>
               <title line>
               <full commit message>
raw
The raw format shows the entire commit exactly as stored in the
           commit object.
           
%H: commit hash
%h: abbreviated commit hash
%T: tree hash
%t: abbreviated tree hash
%P: parent hashes
%p: abbreviated parent hashes

%an: author name
%ae: author email
%ad: author date (format respects --date= option)
%cD: committer date, RFC2822 style
%cr: committer date, relative
%ct: committer date, UNIX timestamp
%ai: author date, ISO 8601 format

%cn: committer name
%ce: committer email
%cd: committer date
%cD: committer date, RFC2822 style
%cr: committer date, relative
%ct: committer date, UNIX timestamp
%ci: committer date, ISO 8601 format


%d: ref names, like the --decorate option of git-log(1)
%e: encoding
%s: subject
%b: body
%N: commit notes
%gn: reflog identity name
%ge: reflog identity email

%Cred: switch color to red
%Cgreen: switch color to green
%Cblue: switch color to blue
%Creset: reset color
%C(...): color specification

%x00: print a byte from a hex code
```
```bash
git log --pretty=raw
git log --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
#给命令起个别名
sudo git config alias.logs "log --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
```
### Commit Limiting
```
--since=<date>, --after=<date>
--until=<date>, --before=<date>
    Show commits older than a specific date.
    
--author=<pattern>, --committer=<pattern>

--grep=<pattern>
    Limit the commits output to ones with log message that matches the specified pattern (regular expression)
-i, --regexp-ignore-case
    Match the regular expression limiting patterns without regard to letter case.
    
--merges
    Print only merge commits. This is exactly the same as --min-parents=2.
--no-merges
    Do not print commits with more than one parent.This is exactly the same as --max-parents=1.
--branches[=<pattern>]
--tags[=<pattern>]
--remotes[=<pattern>]
```
```
git log --before "Sat Aug 30 2014"
git log --before="20 days ago" --date=relative
git log --author=yourname
git log --grep=fix
```
### 可选参数
```
--source
    Print out the ref name given on the command line by which each
    commit was reached.
    
--log-size
    Include a line “log size <number>” in the output for each commit,
    where <number> is the length of that commit’s message in bytes.
    Intended to speed up tools that read log messages from git log
    output by allowing them to allocate space in advance.
    
-L <start>,<end>:<file>, -L :<regex>:<file>
    Trace the evolution of the line range given by "<start>,<end>" 
    (or the funcname regex <regex>) within the <file> <start> and <end> can take one of these forms:
    #number
    If <start> or <end> is a number, it specifies an absolute line number (lines count from 1).
    #/regex/
    This form will use the first line matching the given POSIXregex.
    If <start> is a regex, it will search from the end of the previous -L range, if any, otherwise from the start of file.
```
```
git log -L /express/,/http/:app.js
```
### Common diff 
```
-p      #查看文件的修改内容
--stat  #列出文件的修改行数
git log -p --stat README.md
```

