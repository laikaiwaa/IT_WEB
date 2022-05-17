// pages/test/admin.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:"",
    serachname:{username: '',usercode:'',userkind:'user'},
    admincheckboxmark:'',
    usercheckboxmark:'on'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  getuser(){ 
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/admin/",
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
  onLoad() {
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
  findway:function(event: any){
    var way=event.currentTarget.dataset.src;
    if(way=="quit"){
      this.quit();
    }else if(way=="usehistory"){
      this.usehistory();
    }else if(way=="checkuserform"){
      this.checkuserform();
    }
  },
  checkuserform(){ 
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/"+checkdata['page']+"/",
      data:'\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="code"' +'\r\n' +'\r\n' +checkdata['code']+
      '\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="key"' +'\r\n' +'\r\n' + checkdata['key']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="checkuserform"' +'\r\n' +'\r\n' + 'yes'+
      '\r\n--XXX--',
      header:{
        'content-type':'multipart/form-data; boundary=XXX'
      },
      method:"POST",
      success:function(res:any){    
        wx.setStorageSync('namelist',res.data.usernamelist);
        wx.setStorageSync('pagedata',res.data); 
        self.setData({
          iniuserdata:wx.getStorageSync('userdata'),
          inipagedata:wx.getStorageSync('pagedata')
          });
        wx.redirectTo({
          url: '../test/user',
        });
      }
    });
    
  },
  usehistory(){
    wx.redirectTo({
      url: '../test/usehistory',
    })
  },
  quit(){
    wx.clearStorageSync();
    wx.redirectTo({
      url: '../test/login',
    })
  },
  settxt(e: any){    
    if(e.target.id=='username'){
      this.data.serachname['username']=e.detail.value;
    }else{
      this.data.serachname['usercode']=e.detail.value;
    };
    console.log(e.detail.value); 
  },
  setmark(e: any){ 
    var checkboxid=e.target.dataset.userkindd; 
    if(checkboxid=="admin"){
      if(this.data.serachname.userkind=='admin'){
        this.data.serachname.userkind='user';
        this.setData({
          admincheckboxmark:'',
          usercheckboxmark:'on',
        }) 
      }else{
        this.data.serachname.userkind='admin';
        this.setData({
          admincheckboxmark:'on',
          usercheckboxmark:'',
        }) 
      }
    }else{
      if(this.data.serachname.userkind=='admin'){
        this.data.serachname.userkind='user';
        this.setData({
          admincheckboxmark:'',
          usercheckboxmark:'on',
        }) 
      }else{
        this.data.serachname.userkind='admin';
        this.setData({
          admincheckboxmark:'on',
          usercheckboxmark:'',
        }) 
      }
    };
    console.log(this.data.serachname);
  } ,
  getType:function(e:any){
    let value = e.currentTarget.dataset.type
    this.setData({
    type:value ,
    isSelect: false,
    })
    },
  adminuser(e:any){
    var users=e.currentTarget.dataset.src;
    var self=this;
    var checkdata=wx.getStorageSync('userdata');
    wx.request({
      url:"http://127.0.0.1:81/"+checkdata['page']+"/",
      data:'\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="code"' +'\r\n' +'\r\n' +checkdata['code']+
      '\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="key"' +'\r\n' +'\r\n' + checkdata['key']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="userop"' +'\r\n' +'\r\n' + JSON.stringify(this.data.serachname)+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="adminuserkind"' +'\r\n' +'\r\n' +users+
      '\r\n--XXX--',
      header:{
        'content-type':'multipart/form-data; boundary=XXX'
      },
      method:"POST",
      success:function(res:any){  
        var uppagedata=wx.getStorageSync('pagedata');
        uppagedata.list=res.data.list;
        wx.setStorageSync('pagedata',uppagedata);
        console.log(res.data); 
        self.setData({
          iniuserdata:wx.getStorageSync('userdata'),
          inipagedata:wx.getStorageSync('pagedata')
          });  
      }
    })
  }
})