// pages/test/user.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:"",
    serachname:'',
    namelist:''
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  getuser(){ 
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    if(checkdata['page']=='user' || this.data.serachname!=''){
      var usernamet=''
      console.log("checkkkkkkkkkkk");
      if(this.data.serachname!=''){
        usernamet=this.data.serachname
      }else{
        usernamet=checkdata['username']
      }
      wx.request({
        url:"https://www.kiewaalab.top:442/user/",
        data:{
          code:checkdata['code'],
          key:checkdata['key'],
          username:usernamet
        },
        header:{
          'content-type':'multipart/json'
        },
        method:"GET",
        success:function(res:any){
          wx.setStorageSync('pagedata',res.data);  
          self.setData({
            iniuserdata:wx.getStorageSync('userdata'),
            inipagedata:wx.getStorageSync('pagedata'),
            namelist:wx.getStorageSync('namelist')
            });
        }
      })
    }else{
      console.log("onload",wx.getStorageSync('pagedata')); 
      self.setData({
        iniuserdata:wx.getStorageSync('userdata'),
        inipagedata:wx.getStorageSync('pagedata'),
        namelist:wx.getStorageSync('namelist')
        });
    }; 
  },
  settxt(e: any){    
    this.data.serachname=e.detail.value;
    console.log(e.detail.value); 
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
    }else if(way=="checkform"){
      this.getuser();
    }else if(way=="usehistory"){
      this.usehistory();
    }else if(way=="quit"){
      this.quit();
    }
  },
  back(){
    wx.redirectTo({
      url:"../test/admin"
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
    var pagedata=wx.getStorageSync('pagedata');
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"https://www.kiewaalab.top:442/"+checkdata['page']+'/',
      data:{
        code:checkdata['code'],
        key:checkdata['key'],
        username:pagedata['username'],
        userkind:checkdata['userkind'],
        checkform:formfilename
      },
      header:{
        'content-type':'multipart/json'
      },
      method:"GET",
      success:function(res:any){  
        wx.setStorageSync('pagedata',res.data);
        wx.setStorageSync('checkformmark',1);
        var updata=wx.getStorageSync('pagedata');
        self.setData({
          iniuserdata:wx.getStorageSync('userdata'),
          inipagedata:updata
          }); 
        if(updata['htmlname']=="job_fileslist.html"){
          wx.redirectTo({
            url: '../test/form_fileslist',
          });
        }else if(updata['htmlname']=="job_systemchecklist.html"){
          wx.redirectTo({
            url: '../test/form_syschecklist',
          });
        }else if(updata['htmlname']=="QRcode.html"){
          wx.redirectTo({
            url: '../test/form_qrcodelist',
          });
        }else{
          wx.redirectTo({
            url: '../test/form_qrcodelist',
          });
        }
        
      }
    })
  }


})