// pages/test/login.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
//登录处理
  login(){
    wx.request({
      url:'http://127.0.0.1:81/',
      data:'\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="username"' +
      '\r\n' +
      '\r\nn' +
      '\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="usercode"' +
      '\r\n' +
      '\r\n' +
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="login"' +
      '\r\n' +
      '\r\n1' +
      '\r\n--XXX--',
      header:{
        'content-type':'multipart/form-data; boundary=XXX'
      },
      method:"POST",
      success(res){
        var jd = JSON.parse(JSON.stringify(res.data));
        wx.setStorageSync('userdata',jd);
        if(jd['userkind']=='user'){ 
          wx.redirectTo({
            url: '../test/user',
          })
        }
        
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {

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