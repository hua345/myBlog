### 1.1 安装go-bindata
```
go get -u github.com/go-bindata/go-bindata/...
```
#### 1.2 查看帮助
```
$ go-bindata -version
go-bindata 3.1.1 (Go runtime go1.12.2).
Copyright (c) 2010-2013, Jim Teeuwen.

$ go-bindata
Missing <input dir>

Usage: E:\goCode\bin\go-bindata.exe [options] <input directories>

  -debug
        Do not embed the assets, but provide the embedding API. Contents will still be loaded from disk.
  -fs
        Whether generate instance http.FileSystem interface code.
  -ignore value
        Regex pattern to ignore
  -nocompress
        Assets will *not* be GZIP compressed when this flag is specified.
  -nomemcopy
        Use a .rodata hack to get rid of unnecessary memcopies. Refer to the documentation to see what implications this carries.
  -nometadata
        Assets will not preserve size, mode, and modtime info.
  -o string
        Optional name of the output file to be generated. (default "./bindata.go")
  -pkg string
        Package name to use in the generated code. (default "main")
```
### 2.1 打包静态资源
```
//go:generate go-bindata -o=asset/asset.go -pkg=asset public/...
```
#### 2.2 查看生成的`asset/asset.go`文件
```
// Asset loads and returns the asset for the given name.
// It returns an error if the asset could not be found or
// could not be loaded.
func Asset(name string) ([]byte, error) 

// For example if you run go-bindata on data/... and data contains the
// following hierarchy:
//     data/
//       foo.txt
//       img/
//         a.png
//         b.png
// then AssetDir("data") would return []string{"foo.txt", "img"}
// AssetDir("data/img") would return []string{"a.png", "b.png"}
// AssetDir("foo.txt") and AssetDir("notexist") would return an error
// AssetDir("") will return []string{"data"}.
func AssetDir(name string) ([]string, error)
```
#### 3.1 获取目录文件列表
```golang
const publicDir = "public"
func GetTemplateFilesName(assertPath string) []string {
	var fileNameList []string
	assertFileNameList, err := asset.AssetDir(path.Join(publicDir, assertPath))
	if err != nil {
		panic(err)
	}
	for _, fileItem := range assertFileNameList {
		fileInfo, _ := asset.AssetInfo(path.Join(publicDir, assertPath, fileItem))
		if nil == fileInfo || fileInfo.IsDir() {
			continue
		} else {
			fileNameList = append(fileNameList, fileItem)
		}
	}
	return fileNameList
}
```
#### 3,2 读取文件内容解析模板
```golang
func ParseTemplate(dstPath, srcPath string, data interface{}) {
	templateContent, err := asset.Asset(path.Join(publicDir, srcPath))
	if err != nil {
		log.Println(path.Join(publicDir, srcPath) + " Template File not found.")
		os.Exit(-1)
	}
	srcTemplate, err := template.New(srcPath).Parse(string(templateContent))
	if err != nil {
		panic(nil)
	}
	dstFileStream, err := os.Create(dstPath)
	defer dstFileStream.Close()
	if err != nil {
		panic(nil)
	}

	err = srcTemplate.Execute(dstFileStream, data)
	if err != nil {
		panic(nil)
	}
}
```
