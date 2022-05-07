// pages/test/usehistory.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:"",
    btime:"",
    etime:"",
    serch:""
  },
  changebtime(e: { detail: { value: any; }; }){
    this.setData({btime:e.detail.value});
  },
  changeetime(e: { detail: { value: any; }; }){
    this.setData({etime:e.detail.value,
    serch:"yes"});
  },
  usehistryop:function(event: { currentTarget: { dataset: { src: any; }; }; }){
    var op=event.currentTarget.dataset.src;
    if(op=='serch'){
      console.log(this.data.btime);
      this.getudata();
    }else if(op=='back'){
      wx.redirectTo({
        url: '../test/user'
      });
    }
  },
  getudata(){ 
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
      '\r\nContent-Disposition: form-data; name="usehistory"' + '\r\n' + '\r\nyes' +
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="htmlname"' +'\r\n' +'\r\n' +
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="btime"' +'\r\n' +'\r\n' +  this.data.btime+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="etime"' +'\r\n' +'\r\n' + this.data.etime+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="serch"' +'\r\n' +'\r\n' + this.data.serch+
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
    this.getudata();
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

  }
})