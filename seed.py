from models import User, Post, Tag, PostTag, db 
from app import app

# create all tables
db.drop_all()
db.create_all()

#if table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

alan = User(first_name="Alan", last_name="Alda", image_url="https://images.unsplash.com/photo-1678780593184-c71d50923fd9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDR8SnBnNktpZGwtSGt8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=60")
joel = User(first_name="Joel", last_name="Burton", image_url="https://images.unsplash.com/photo-1668174206552-cc53001e480b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDExfEpwZzZLaWRsLUhrfHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60")
jane = User(first_name="Jane", last_name="Smith", image_url="https://images.unsplash.com/photo-1678415488427-1b9470865455?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDEyfEpwZzZLaWRsLUhrfHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60")

post1 = Post(title='First Post', content='This is the very first post.',user_id=1)
post2 = Post(title='Second Post', content='This is the second post.',user_id=1)
post3 = Post(title='Third Post', content='This is the third post.',user_id=2)

tag1 = Tag(name='fun')
tag2 = Tag(name='happy')

posttag1 = PostTag(post_id=1, tag_id=1)
posttag2 = PostTag(post_id=1, tag_id=2)

# add new objects to session, so they'll persist
db.session.add(alan)
db.session.add(joel)
db.session.add(jane)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(posttag1)
db.session.add(posttag2)



# commit, otherwise never gets saved
db.session.commit()