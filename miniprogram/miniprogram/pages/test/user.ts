// pages/test/user.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:""
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  getuser(){ 
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/user/",
      data:{
        code:checkdata['code'],
        key:checkdata['key'],
        username:checkdata['username']
      },
      header:{
        'content-type':'multipart/json'
      },
      method:"GET",
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
  onLoad () { 
     this.getuser();
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
  /**
   * 操作导向
   * @param event 
   */
  findway:function(event: { currentTarget: { dataset: { src: any; }; }; }){
    var way=event.currentTarget.dataset.src;
    if(way=="back"){
      this.back();
    }else if(way=="quit"){
      this.quit();
    }else if(way=="usehistory"){
      this.usehistory();
    }
  },
  back(){
    var a=this.getuser;
    wx.request({
      url:'http://127.0.0.1:81/user/',
      data:{
        back:"yes"
      },
      header:{
        'content-type':'multipart/json'
      },
      method:"GET",
      success(res){
        console.log(res.data);
        a;
      }
    })
  },
  quit(){
    wx.clearStorageSync();
    wx.redirectTo({
      url: '../test/login',
    })
  },
  usehistory(){
    wx.redirectTo({
      url: '../test/usehistory',
    })
  },
  /**
   * 创建表
   */
  buildform:function(event: { currentTarget: { dataset: { src: any; }; }; }){
    var formkind=event.currentTarget.dataset.src;
    if(formkind=="form_fileslist"){
      wx.redirectTo({
        url: '../test/form_fileslist',
      })
    }else if(formkind=="form_syschecklist"){
      wx.redirectTo({
        url: '../test/form_syschecklist',
      })
    }else{
      wx.redirectTo({
        url: '../test/form_qrcodelist',
      })
    }
  },
  checkform:function(e:any){
    var formfilename=e.currentTarget.dataset.src;
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/user/",
      data:{
        code:checkdata['code'],
        key:checkdata['key'],
        username:checkdata['username'],
        userkind:checkdata['userkind'],
        checkform:formfilename
      },
      header:{
        'content-type':'multipart/json'
      },
      method:"GET",
      success:function(res){  
        wx.setStorageSync('pagedata',res.data);
        wx.setStorageSync('checkformmark',1);
        console.log(res.data);
        var pagdata=wx.getStorageSync('pagedata');
        self.setData({
          iniuserdata:wx.getStorageSync('userdata'),
          inipagedata:pagdata
          }); 
        if(pagdata['htmlname']=="job_fileslist.html"){
          wx.redirectTo({
            url: '../test/form_fileslist',
          });
        }else if(pagdata['htmlname']=="job_systemchecklist.html"){
          wx.redirectTo({
            url: '../test/form_syschecklist',
          });
        }
        
      }
    })
  }


})