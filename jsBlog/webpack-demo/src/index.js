// import _ from 'lodash';
import sayHi from './Hi';
import math from './math'

function component() {
  var element = document.createElement("div");

  // Lodash（目前通过一个 script 脚本引入）对于执行这一行是必需的
  // element.innerHTML = _.join(["Hello", "webpack"], " ");
  element.innerHTML = sayHi("webpack") + math.add(3,4)
  return element;
}

document.body.appendChild(component());
