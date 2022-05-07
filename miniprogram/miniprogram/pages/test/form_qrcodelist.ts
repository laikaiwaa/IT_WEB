// pages/test/form_qrcodelist.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:"",
  },
  getuser(){ 
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/user/",
      data:'\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="code"' +'\r\n' +'\r\n' +checkdata['code']+
      '\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="key"' +'\r\n' +'\r\n' + checkdata['key']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="username"' +'\r\n' +'\r\n' + checkdata['username']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="form_qrcodelist"' + '\r\n' + '\r\nyes' +
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="htmlname"' +'\r\n' +'\r\n' +
      '\r\n--XXX--',
      header:{
        'content-type':'multipart/form-data; boundary=XXX'
      },
      method:"POST",
      success:function(res){
        wx.setStorageSync('pagedata',res.data),
        console.log(res.data),
        self.setData({
          iniuserdata:wx.getStorageSync('userdata'),
          inipagedata:wx.getStorageSync('pagedata')
          });
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    var u=require('../../utils/html5-qrcode.min.js');
    this.getuser()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },
  findway:function(event: any){
    var way=event.currentTarget.dataset.src;
    if(way=="back"){ 
      wx.redirectTo({
        url: '../test/user'
      });
    }
  },
  settxt(e: any){ 
    var temp=wx.getStorageSync('pagedata');
    temp.formcantain[e.target.id]=e.detail.value;
    console.log(e.detail.value);
    wx.setStorageSync('pagedata',temp);
    this.setData({ 
      inipagedata:wx.getStorageSync('pagedata')
      });
  },
/**
 * ####### Form Add #######
 */ 
 successm:function(e: any){

    },
   /**
 * ####### Scan History #######
 */    
  judfe(id:any,res:any){
    var data = this.getTableContent(id)
    var index = -1;
    for (var j = 0; j < data.length; ++j) {
        if (data[j][1] == res) {
              index = j;
        }
  }
  if (index == -1) {
          data.push([data.length+1,res]);
          this.inserr(id,res)
      } 
},

 inserr(mytable:any,res:any){ 
    var g=mytable.insertRow();
    var p=g.insertCell();
    p.innerHTML=mytable.rows.length;
    p=g.insertCell();
    p.innerHTML=res; 
},

  getTableContent(mytable:any){ 
  var data = [];
  for(var i=0,rows=mytable.rows.length; i<rows; i++){
    for(var j=0,cells=mytable.rows[i].cells.length; j<cells; j++){
      if(!data[i]){
        data[i] = new Array();
      }
      data[i][j] = mytable.rows[i].cells[j].innerHTML;
    }
  }
  return data;
},
 setResult(label:any, result:any) {
    console.log(result);  
    label.textContent = result; 
    label.style.color = 'teal'; 
    label.highlightTimeout = setTimeout(() => label.style.color = 'inherit', 100);
},
/**
 *  ####### Scan Function #######
 */
start(){
     
}
/**
 * ####### Web Cam Scanning #######
 */
// 
   
})