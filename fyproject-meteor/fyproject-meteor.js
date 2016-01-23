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
