"""
Todos: 	
	1. Make the program run way faster by seperating the utilities the program provides into an assembly line. 
	2. Make sure that the program is structured such that each user operation requires as few function calls 
	   as possible, and do the loading of required dictionaries and API calls inside as much as possible. 
	3. Think of a way to save each track's audio features in a tidy way and start analyzing 
"""

import random 
import config 
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials



class SpotifyUtils:
	def __init__(self):
		self.token = util.prompt_for_user_token(
		config.MY_USERNAME,
		config.SCOPE,
		client_id=config.KEY,
		client_secret=config.SECRET,
		edirect_uri=config.REDIRECT_URL)

		self.sp = spotipy.Spotify(auth=token)
		self.sp.trace = False 

	""" 
		Gets the top tracks of the user and spits out a dictionary containing a lot of information on the tracks
		and the artist. This is based on three different terms of top tracks: the recent "short term", a 
		longer "medium_term", and, the longest "long_term" (since you started using spotify probably)
	"""
	def get_top_tracks_based_on_term(self, range, num_tracks):
		if self.token:
			ranges = ['short_term', 'medium_term', 'long_term']
			if range == ranges[0]:
				return self.sp.current_user_top_tracks(time_range=range, limit=num_tracks)
			elif range == ranges[1]:
				return self.sp.current_user_top_tracks(time_range=range, limit=num_tracks)
			elif range == ranges[2]:
				return self.sp.current_user_top_tracks(time_range=range, limit=num_tracks)
			else:
				print("Incorrect range...")
		else:
			print("Can't get token for", config.MY_USERNAME)

	""" 
		Feed the function the top tracks-id and its artist-id dictionary and it spits out a dictionary 
		containing the recommended song and the artist. It uses the top tracks, top artists, and recommended 
		genres as seed, and takes one random value of each to make the recommendations diverse. 
	"""
	def get_recommendedations(self, track_dict, num_tracks):
		top_artist_id_list = []
		top_track_id_list = []
		rec_song = {}
		rec_artist = {}

		for i, item in enumerate(track_dict['items']):
			top_artist_id_list.append(item['artists'][0]['id'])
			top_track_id_list.append(item['id'])

		if self.token:
			random_artist_seed = random.choice(top_artist_id_list)
			random_song_seed = random.choice(top_track_id_list)
			random_genre_seed = random.choice(self.sp.recommendation_genre_seeds()['genres'])
			recommendations_list_tracks = self.sp.recommendations(
			seed_artists=[random_artist_seed], seed_tracks=[random_song_seed],
			seed_genres=[random_genre_seed], limit=num_tracks
			)
			
			for i, track in enumerate(recommendations_list_tracks['tracks']):
				rec_song[track['name']] = track['id']
				rec_artist[track['artists'][0]['name']] = track['artists'][0]['id']
			return (rec_song, rec_artist)
		else:
			print("Can't get token for", MY_USERNAME)
			return None 

	# Spits out any playlist's song-id dictionary 
	def get_playlist_tracks(self, playlist_id):
		song_id_newnew_dict = {}
		offset = 0
		if self.token: 
			while True:
				tracks_list = self.sp.playlist_tracks(
					playlist_id, offset=offset,
					limit=100, fields='items.track.name, items.track.id'
				)
				offset += len(tracks_list['items'])
				for track_item in tracks_list['items']:
					if track_item['track'] != None:
						song_id_newnew_dict[track_item['track']['name']] = track_item['track']['id'] 
				if(len(tracks_list['items']) == 0):
					break 
			return song_id_newnew_dict

	# Removes recommendations which are already contained within any of the existing playlists and 
	# returns a filtered recommendation dictionary 
	def remove_recommendations_which_exists_already(self, rec_dictionary, newnew_dict, rap_dict, rock_dict,
													edm_dict, metal_dict, bollywood_dict, nepali_dict,
													pop_dict, funknchill_dict
	):
		filtered_recommendations = {}
		for rec_key in rec_dictionary:

			if(not rec_dictionary[rec_key] in newnew_dict.values() and not rec_dictionary[rec_key]
			in rap_dict.values() and not rec_dictionary[rec_key] in rock_dict.values() and not
			rec_dictionary[rec_key] in edm_dict.values() and not rec_dictionary[rec_key] in 
			metal_dict.values() and not rec_dictionary[rec_key] in bollywood_dict.values() and not 
			rec_dictionary[rec_key] in nepali_dict.values() and not rec_dictionary[rec_key] in
			pop_dict.values() and not rec_dictionary[rec_key] in funknchill_dict.values()
			):
				filtered_recommendations[rec_key] = rec_dictionary[rec_key]
		return filtered_recommendations

	""" 
		Use the track function to look up any song in the newnew dictionary and get its id. Using that, we
		can extract the artist's id and query the artist's genres. Returns a list of the artist's 
		(and therefore the track's) list of genres 
	"""
	def get_track_genre(self, id):
		if self.token:
			track = self.sp.track(id)
			track_artist_id = track['artists'][0]['id']
			artist_info = self.sp.artist(track_artist_id)
			return artist_info['genres']

	"""
		Cleans up my master playlist based on other general playlists. This takes a while to run as there are
		lots of heavy functions at use. Note: you can only add a maximum of 100 tracks per request 
		(i = 100 always). I used this function to transfer my messy master playlist of 1337 songs to the
		appropriate genres.
	"""
	def clean_up_newnew_playlist(self, newnew): 
		rap_uri_ids = []
		rock_uri_ids = []
		edm_uri_ids = []
		metal_uri_ids = []
		bollywood_uri_ids = []
		nepali_uri_ids = []
		pop_uri_ids = []
		funknchill_uri_ids = []

		"""
			Get 8 lists of track uri's for each genre of song in my master playlist. The genre search is
			designed to be as broad as possible to catch as many songs in 100 iterations.
		""" 
		for i, song in enumerate(newnew):
			if i < 100:
				list_of_genres = self.get_track_genre(newnew[song])
				if list_of_genres != []:
					for genre in list_of_genres:
						if "rap" in genre or "hip hop" in genre or "trap" in genre:
							rap_uri_ids.append(newnew[song])
							break 
						elif "edm" in genre or "techno" in genre or "disco" in genre or "house" in genre:
							edm_uri_ids.append(newnew[song])
							break 
						elif "bollywood" in genre or "filmi" in genre:
							bollywood_uri_ids.append(newnew[song])
							break 
						elif "rock" in genre or "blues" in genre or "instrumental":
							rock_uri_ids.append(newnew[song])
							break 
						elif "nepali" in genre:
							nepali_uri_ids.append(newnew[song])
							break 
						elif "metal" in genre:
							metal_uri_ids.append(newnew[song])
							break 
						elif "pop" in genre and "rap" not in genre or "r&b" in genre:
							pop_uri_ids.append(newnew[song])
							break 
						elif "funk" in genre or "soul" in genre or "chill" in genre:
							funknchill_uri_ids.append(newnew[song])
							break 

		# Adds songs to the relevant playlists while removing those exact songs from newnew playlist 
		if self.token: 
			if rap_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.RAP_ID, rap_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, rap_uri_ids, snapshot_id=None
				)

			if rock_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.ROCK_ID, rock_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, rock_uri_ids, snapshot_id=None
				)
				
			if edm_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.EDM_ID, edm_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, edm_uri_ids, snapshot_id=None
				)
			
			if metal_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.METAL_ID, metal_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, metal_uri_ids, snapshot_id=None
				)
			
			if bollywood_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.BOLLYWOOD_ID, bollywood_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, bollywood_uri_ids, snapshot_id=None
				)
				
			if nepali_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.NEPALI_ID, nepali_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, nepali_uri_ids, snapshot_id=None
				)
				
			if pop_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.POP_ID, pop_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, pop_uri_ids, snapshot_id=None
				)

			if funknchill_uri_ids != []:
				self.sp.user_playlist_add_tracks(
					config.MY_USERNAME, config.FUNK_N_CHILL_ID, funknchill_uri_ids, position=None
				)
				self.sp.user_playlist_remove_all_occurrences_of_tracks(
					config.MY_USERNAME, config.NEWNEW_ID, funknchill_uri_ids, snapshot_id=None
				)

	"""
	 	Lets the users delete any tracks they don't want in the final recommendation list until they are
		satisfied and adds it to the newnew playlist.
	"""
	def review_tracks_and_add_to_newnew(self, song_rec_dictionary):
		new_dict = dict(song_rec_dictionary)
		remove_songs = [] 

		for i, key in enumerate(song_rec_dictionary):
			print(i+1, "Filtered Rec list", key, song_rec_dictionary[key])

		print("""
			Copy/Paste the key of the song you don't want to add to datnewnew. The recommended songs are
			printed above for reference. These songs will be added straight to the newnew playlist, and then
			you can call the clean_up_newnew_playlist function after that to move its songs to the appropriate
			destinations. Type "done" in this exact format once you're done filtering songs for yourself.
		""")

		while True:
			user_input = input()
			if user_input == "done":
				break 
			if user_input in new_dict.values():
				remove_songs.append(user_input)
			else:
				print("Wrong input, try again or write \"done\"")

		song_name_list = list(new_dict.keys()) 
		song_id_list = list(new_dict.values()) 

		if remove_songs != []:
			for song_removal_id in remove_songs:
				song_name = song_name_list[song_id_list.index(song_removal_id)]
				del new_dict[song_name]

		adder_ids = list(new_dict.values())
		if token:
			self.sp.user_playlist_add_tracks(config.MY_USERNAME, config.NEWNEW_ID, adder_ids, position=None)

	# Set the iterator and return and returns a list of PlaylistTrack objects with the features set in place 
	def set_iterator(self, iterator):
		playlist_objects = []
		if iterator != None:
			for song in iterator:
				if self.token:
					features = sp.audio_features([iterator[song]])[0]
					track = PlaylistTrack(
							iterator[song], song,  
							features['energy'], features['liveness'], features['tempo'], 
							features['speechiness'], features['acousticness'], features['instrumentalness'],
							features['time_signature'], features['danceability'], features['key'],
							features['duration_ms'], features['loudness'], features['valence'],
							features['mode'])

					playlist_objects.append(track)
			return playlist_objects 


	def analyze_playlist(self):
		rap_playlist_dict = get_playlist_tracks(config.RAP_ID)
		


























