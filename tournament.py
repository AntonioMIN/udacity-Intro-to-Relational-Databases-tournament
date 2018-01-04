#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(database="tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db=connect()
    c=db.cursor()
    c.execute("delete from matches;")
    c.execute("update players set match=0;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db=connect()
    c=db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db=connect()
    c=db.cursor()
    c.execute("select count(*) from players;")
    return c.fetchall()[0][0]
    db.close()

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db=connect()
    c=db.cursor()
    c.execute("insert into players (name, match) values(%s, 0);",(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db=connect()
    c=db.cursor()
    c.execute("select players.id, players.name, count(winner) as wins, players.match as matches from players left join matches on players.id=matches.winner group by players.id order by wins desc;")
    return c.fetchall()
    db.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db=connect()
    c=db.cursor()
    c.execute("insert into matches (winner, loser) values(%s,%s);",(winner, loser,))
    c.execute("update players set match=match+1 where id=%s or id=%s",(winner,loser,))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db=connect()
    c=db.cursor()

    players=playerStandings()
    count=countPlayers()
    ret=[]
    vis=[]
    for i in range(count):
        vis.append(0)
    for i in range(count):
        if vis[i]==1:
            continue
        for j in range(i+1, count):
            c.execute("select id from matches where (winner=%s and loser=%s) or (winner=%s and loser=%s)",(players[i][0],players[j][0],players[i][0],players[j][0],))
            t=c.fetchall()
            if len(t)==0:
                ret.append((players[i][0],players[i][1],players[j][0],players[j][1]))
                vis[i]=1
                vis[j]=1
                break
    return ret
    db.close()