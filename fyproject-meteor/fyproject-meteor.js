articles = new Mongo.Collection('articles');
if (Meteor.isClient) {
   var handle;
  Deps.autorun(function(){
    handle=Meteor.subscribeWithPagination('articles', 5)
  });
  Template.viewArticles.helpers  ({ 
        //NOTE : 'event' is the name of variable from html template
        'article' : function () {
             //returns list of Objects for all Events
             return articles.find({});
         }
        });
  
  Template.viewArticles.events({
    'click .btn':function(){
      handle.loadNextPage();
    }
  })
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    Meteor.publish("articles", function(limit){
      return articles.find({}, {limit:limit});
    }); 

  });
}





/* OLD, Perfectly Working code
if (Meteor.isClient) {
  // counter starts at 0
  Session.setDefault('counter', 0);

  Template.viewArticles.helpers  ({ 
        //NOTE : 'event' is the name of variable from html template
        'article' : function () {
             //returns list of Objects for all Events
             return articles.find().fetch();
         }
});
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  	
  });
}
articles = new Mongo.Collection('articles');
*/
