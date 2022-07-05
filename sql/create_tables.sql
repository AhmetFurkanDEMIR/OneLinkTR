

CREATE TABLE public.tbl_users (
	user_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	user_name varchar(30) NULL,
	user_surname varchar(30) NULL,
	user_phone bpchar(11) NULL,
	user_email varchar(50) NULL,
	user_password varchar(90) NULL,
	user_isdeleted int4 NULL,
	user_confirmed int4 NULL,
	user_countattack int4 NULL,
	user_appcount int4 NULL,
	CONSTRAINT tbl_users_pkey PRIMARY KEY (user_id),
	CONSTRAINT tbl_users_un UNIQUE (user_email),
	CONSTRAINT tbl_users_un0 UNIQUE (user_phone)
);


CREATE TABLE public.tbl_apps (
	app_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	user_id int4 NULL,
	app_name varchar(30) NULL,
	CONSTRAINT tbl_apps_pkey PRIMARY KEY (app_id)
);


ALTER TABLE public.tbl_apps ADD CONSTRAINT tbl_apps_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tbl_users(user_id);

CREATE TABLE public.tbl_links (
	link_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	app_id int4 NULL,
	link_name varchar(30) NULL,
	link_url varchar(130) NULL,
	CONSTRAINT tbl_links_pkey PRIMARY KEY (link_id)
);


ALTER TABLE public.tbl_links ADD CONSTRAINT tbl_links_app_id_fkey FOREIGN KEY (app_id) REFERENCES public.tbl_apps(app_id);