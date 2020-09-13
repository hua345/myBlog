`约定大于配置`，一个约定到的目录结构方便阅读源码，统一项目风格。
#### Github上约定好的Go应用程序项目的基本布局
[https://github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout)

#### `/cmd`
项目main函数文件目录

这个目录下面，每个文件在编译之后都会生成一个可执行的文件，比如`/cmd/myapp`。

不要把很多的代码放到这个目录下面，这里面的代码尽可能简单。

如果源码可以被其他项目使用可以放到`pkg`目录。

如果代码不希望被其他项目使用可以放到`/internal`目录。
#### `/internal`
项目私有代码和依赖库代码目录。

把实际项目代码放到`/internal/app`目录，比如`/internal/app/myapp`

项目共享的代码放到`/internal/pkg`目录，比如`/internal/pkg/myprivlib`
#### `/pkg`
一些通用的可以被其他项目所使用的代码，放到这个目录下面

#### `/vendor`
项目依赖的其他第三方库

#### `/api`
OpenAPI/Swagger specs, JSON schema files, protocol definition files.

#### `/web`
Web application specific components: static web assets, server side templates and SPAs.

#### `/configs`
Configuration file templates or default configs.

#### `/build`
Packaging and Continuous Integration.

Put your cloud (AMI), container (Docker), OS (deb, rpm, pkg) 
package configurations and scripts in the /build/package directory.
#### `/deployments`
IaaS, PaaS, system and container orchestration deployment configurations
 and templates (docker-compose, kubernetes/helm, mesos, terraform, bosh).

#### `/docs`
Design and user documents (in addition to your godoc generated documentation).

#### `/examples`
Examples for your applications and/or public libraries.

### Directories You Shouldn't Have
#### `/src`
> Some Go projects do have a src folder, 
but it usually happens when the devs came from the Java world where it's a common pattern.
If you can help yourself try not to adopt this Java pattern.
You really don't want your Go code or Go projects to look like Java :-)

>  The $GOPATH environment variable points to your (current) workspace 
(by default it points to $HOME/go on non-windows systems). 
This workspace includes the top level`/pkg`, `/bin` and `/sr`c directories.
 Your actual project ends up being a sub-directory under `/src`, 
 so if you have the`/src`directory in your project the project path will look like this: 
 `$GOPATH/src/your_project/src/your_code.go`.
