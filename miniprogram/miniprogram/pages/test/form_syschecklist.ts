// pages/test/form_syschecklist.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    iniuserdata:"",
    inipagedata:"",
    tempdate:{},
    filenamelist:[{}]
  },

  /**
   * 生命周期函数--监听页面加载
   */
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
      '\r\nContent-Disposition: form-data; name="form_syschecklist"' + '\r\n' + '\r\nyes' +
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
  setmark(e: any){ 
    var temp=wx.getStorageSync('pagedata');  
    var checkboxid=e.target.dataset.id;
    console.log(checkboxid);
    console.log(temp.formcantain[checkboxid]);
    if(temp.formcantain[checkboxid]==""){
      temp.formcantain[checkboxid]="on";
      console.log("checkon");
    }else{
      temp.formcantain[checkboxid]="";
      console.log("checknone");
    }  
    wx.setStorageSync('pagedata',temp);
    
    this.setData({ 
      inipagedata:wx.getStorageSync('pagedata')
      });
  },
  successm:function(e: any){ 
    var filenamelist=wx.getStorageSync('filenamelist');
    var filenum=filenamelist.length;
    var filelength=0;
    if(filenamelist.length!=0){ 
      (async ()=>{
        for(var i in filenamelist){
          filelength=filelength+1; 
          if (filelength==filenum){
            await this.upfiles(e,filenamelist[i],1);
          }else{
            await this.upfiles(e,filenamelist[i],0);
          }
        }
      })()
      wx.removeStorageSync('filenamelist');
    }else{
      this.upformdata(e);
    }
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
   * 上传文件
   */
  upfiles:function(e: any,filenamelist:any,filelength:any){
    return new Promise((resolve)=>{ 
      var self=this;
      var way=e.currentTarget.dataset.src;  
      console.log(filenamelist,"filenamelist");
      var checkdata=wx.getStorageSync('userdata');
      var formdata=wx.getStorageSync('pagedata');
      formdata.formcantain['savemode']=way;
      var fileaddress=wx.getStorageSync('fileaddress');
      console.log("fileaddress",fileaddress);
      wx.uploadFile({ 
        url:"http://127.0.0.1:81/user/",
        filePath:filenamelist.path,
        name:"upchosefiles",
        formData: {
          'chosefiles': 'yes',
          'code':checkdata['code'],
          'key':checkdata['key'],
          'username':checkdata['username'],
          'formcantain':JSON.stringify(formdata),
          'upfilename':filenamelist.name,
          'onlyfile':'yes',
          'fileaddress':fileaddress
        },
        success (res){ 
          wx.setStorageSync('fileaddress',res.data);
          console.log("AAAAAAAAA",filelength);
          if(filelength>0){
            self.upformdata(e);
            wx.redirectTo({
              url: '../test/user'
            });
          }
          resolve("");
        }
      }) 
    })
    
  },
  /**
   * 选择文档
   */
  selectfile(){
    var self=this;
    wx.chooseMessageFile({
      count:10,
      success(res){
        var filist=res.tempFiles;
        console.log(filist);
        var tempfilenamelist=[];
        for(var x in filist ){ 
          tempfilenamelist.push(filist[x]);
        };
        self.setData({ 
            filenamelist:tempfilenamelist,
          });
        wx.setStorageSync('filenamelist',tempfilenamelist)
      }
    })
  }
})