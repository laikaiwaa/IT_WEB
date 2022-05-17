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
    var checkformmark=wx.getStorageSync('checkformmark');
    if(checkformmark==1){
      this.setData({
        iniuserdata:wx.getStorageSync('userdata'),
        inipagedata:wx.getStorageSync('pagedata')
        });
        wx.setStorageSync('checkformmark',0);
    }else{
      this.getuser()
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow(){
    var d=wx.getStorageSync('pagedata');
    console.log("debug",d);
    d.formcantain.codelist=JSON.parse(d.formcantain.codelist);
    this.setData({ 
      /**
       * scanres:wx.getStorageSync('scandatas')
       */
      inipagedata:d
    });
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
    
    wx.setStorageSync('pagedata',temp);
    console.log("settxt",temp);
    this.setData({ 
      inipagedata:wx.getStorageSync('pagedata')
      });
  },
/**
 * ####### Form Add #######
 */ 
successm:function(e: any){
    this.upformdata(e);
},
/**
   * 
   * 上传基础信息 
   */
  upformdata(e: any){
    var way=e.currentTarget.dataset.src;
    var checkdata=wx.getStorageSync('userdata');
    var formdata=wx.getStorageSync('pagedata');
    formdata.formcantain['savemode']=way; 

    wx.request({
      url:"http://127.0.0.1:81/user/",
      data:'\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="code"' +'\r\n' +'\r\n' +checkdata['code']+
      '\r\n--XXX' +
      '\r\nContent-Disposition: form-data; name="key"' +'\r\n' +'\r\n' + checkdata['key']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="username"' +'\r\n' +'\r\n' + checkdata['username']+
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="htmlname"' +'\r\n' +'\r\n' +
      '\r\n--XXX--'+
      '\r\nContent-Disposition: form-data; name="formcantain"' +'\r\n' +'\r\n' +JSON.stringify(formdata)+
      '\r\n--XXX--',
      header:{
        'content-type':'multipart/form-data; boundary=XXX'
      },
      method:"POST",
      success:function(res){
        wx.setStorageSync('pagedata',res.data),
        console.log(res.data),
        wx.redirectTo({
          url: '../test/user'
        });
      }
    });
  },
/**
   * 扫码
   */
  scan(){
    var self=this;
    wx.scanCode({
      success(res){  
        var datas=wx.getStorageSync('pagedata');  
        var len=0;
        if(datas.formcantain.codelist.length>0){
          console.log("debuggg",datas.formcantain.codelist);
          var codelist=JSON.parse(datas.formcantain.codelist);
          len=codelist.length;
        };
        var index = -1;
        for (var j = 0; j < len; ++j) { 
            if (codelist[j].name == res.result) {
                  index = j;
            }
        }; 
        if (index == -1) {
                if(len==0){
                  codelist=[{id:len+1,name:res.result}];
                }else{ 
                  codelist.push({id:len+1,name:res.result});
                  console.log('new',codelist);
                } 
            };
        datas.formcantain.codelist=JSON.stringify(codelist) ;
        wx.setStorageSync('pagedata',datas);
        self.onShow();
      }
    })
  }
   
})