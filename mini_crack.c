/*    Copyright 2004-2018 Universite de Sherbrooke 
 *
 *    Auteur: Frederic Mailhot
 *
 *    Pour faire fonctionner ce petit programme de decouverte
 *    de mots de passe, vous devez modifier 2 procedures:
 *    - run_dict:  utiliser correctement l'appel a crypt(), ligne 129
 *    - run_exhaustif: corriger ici aussi l'appel a crypt(), ligne 163
 *
 *    La procédure decryption est fournie et détermine les chaines de caracteres suivantes:
 *          user_name  (le nom de l'usager (son login))
 *          salt       (le salt utilise pour encrypter le mot de passe)
 *          encrypted_passwd (le mot de passe encrypte par crypt en utilisant
 *                            les extensions GNU -> faire 'man crypt' pour
 *                            plus de renseignements, et voir GNU EXTENSION)
 *    La procedure decryption lit le fichier de mots de passe une ligne a la
 *    fois, et extrait les 3 chaines de caracteres mentionnees plus haut pour chacune des lignes.
 */



#define _XOPEN_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#define SIZE 1024

char pass_file[SIZE];
char dict_file[SIZE];
FILE *pass_file_ptr;
FILE *dict_file_ptr;
char dict_word[SIZE];
char tmp_dict_word[SIZE];
int verbose = 0;
int exhaustif = 0;
int dict_present = 0;
int fichier_exhaustif_present = 0;
char fichier_exhaustif[SIZE];
char caracteres_exhaustifs[SIZE];
char recherche[SIZE];
int niveau_actuel = 0;
int nombre_de_caracteres_exhaustifs = 0;
char salt[13];
char encrypted_passwd[SIZE];
char *test_encrypted_passwd;
char user_name[SIZE];
int found_it = 0;

void err_message() {
  fprintf(stdout, "Usage: mini_crack [options]\n");
  fprintf(stdout, "\t-help (impression de ce message)\n");
  fprintf(stdout, "\t-v ou -verbose (donne plus d\'information)\n");
  fprintf(stdout, "\t-pw fichier_de_mot_de_passe\n");
  fprintf(stdout, "\t-dict fichier_dictionnaire\n");
  fprintf(stdout, "\t-xl longueur de la recherche exhaustive (nombre entier)\n");
  fprintf(stdout, "\t-xc fichier_de_chaine_de_caracteres\n");
  fprintf(stdout, "\t    fichier contenant les caracteres a utiliser\n");
  fprintf(stdout, "\t    pour la recherche exhaustive\n");
}

int open_files()
{
  FILE *exh_ptr;
  int i;

  pass_file_ptr = fopen(pass_file,"r");
  if (!pass_file_ptr) {
    fprintf(stdout,
            "Impossible d'ouvrir le fichier de mots de passe%s\n",
            pass_file);
    return(0);
  }

  if (dict_present) {
    dict_file_ptr = fopen(dict_file,"r");
    if (!dict_file_ptr) {
      fprintf(stdout,
              "Impossible d'ouvrir le fichier dictionnaire %s\ni",
              dict_file);
      return(0);
    }
    fclose(dict_file_ptr);
  }

  if (fichier_exhaustif_present) {
    exh_ptr = fopen(fichier_exhaustif,"r");
    if (!exh_ptr) {
      fprintf(stdout,
              "Impossible d'ouvrir le fichier de caracteres exhaustifs %s\n",
	      fichier_exhaustif);
      return(0);
    } else {
      fgets(caracteres_exhaustifs,SIZE,exh_ptr);
      for (i = 0; ((i<SIZE) 
                   && (caracteres_exhaustifs[i] != '\n') 
		   && (caracteres_exhaustifs[i] != '\0')); i++);
      caracteres_exhaustifs[i] = '\0';
      nombre_de_caracteres_exhaustifs = strlen(caracteres_exhaustifs);
      fclose(exh_ptr);
    }
  }
	

  return(1);
}

void run_dict()
{
  int i;

  if (!dict_present) {
    return;
  }

  dict_file_ptr = fopen(dict_file,"r");
  while(!found_it && fgets(dict_word,SIZE,dict_file_ptr)) {

    for (i = 0; ((i<SIZE) 
                  && (dict_word[i] != '\n') 
                  && (dict_word[i] != '\0')); i++) {
      tmp_dict_word[i] = dict_word[i];
    }
    tmp_dict_word[i] = '\0';

    /*
        La variable tmp_dict_word contient une chaîne de caractères qui représente l'un des mots du dictionnaire
    */

    test_encrypted_passwd = (char *) crypt(tmp_dict_word, salt);
    if (!strcmp(test_encrypted_passwd, encrypted_passwd)) {
      fprintf (stdout, 
               "----Usager: %s, Mot de passe: \"%s\"\n", 
               user_name, 
               tmp_dict_word);
      fflush(stdout);
      found_it = 1;
    }


    if (verbose) {
      fprintf(stdout, "\tSalt: %s\n", salt);
      fprintf(stdout, "\tMot de passe: %s\n", tmp_dict_word);
      fprintf(stdout, "\tEncryption: %s\n", test_encrypted_passwd);
      fprintf(stdout, "\tSequence du passwd: %s\n", encrypted_passwd);
      fflush(stdout);
    }
  }
}

void run_exhaustif(int niveau)
{
  int i;

  if (exhaustif == 0) {
    return;
  }

  if (niveau == 0) {
    recherche[exhaustif] = '\0';
    /*
        La variable recherche comprend une chaîne de caractères qui représente l'une des séquences à valider (l'une de celles incluses dans la recherche exhaustive)
    */
    test_encrypted_passwd = (char *) crypt(recherche, salt);
    if (!strcmp(test_encrypted_passwd, encrypted_passwd)) {
      fprintf (stdout, 
              "----Usager: %s, Mot de passe: \"%s\"\n", 
              user_name, 
              recherche);
      fflush(stdout);
      found_it = 1;
    }

    if (verbose) {
      fprintf(stdout, "\tMot de passe exhaustif: %s\n", recherche);
      fflush(stdout);
    }

    return;
  }

  for (i = 0; (!found_it && (i < nombre_de_caracteres_exhaustifs)); i++) {
    recherche[exhaustif-niveau] = caracteres_exhaustifs[i];
    run_exhaustif(niveau - 1);
  }
}


/*
    decryption va lire une ligne à la fois dans le fichier shadow
    et extrait les éléments suivants:
      user_name:  nom de l'usager
      salt: valeur du SALT (vous pouvez observer la valeur du SALT pour déterminer comment cette chaîne de caractères est utilisée)  (lire sur crypt sera utile)
      encrypted_passwd: hash du mot de passe de l'usager

    Ces variables (globales) sont utilisées pour la recherche par dictionnaire et par force brute (run_dict) et (run_exhaustif)
    Vous devez déterminer comment appeler la fonction crypt() dans ces deux procédures (run_dict) et (run_exhaustif)
*/
void decryption() {
  char passwd_line[SIZE];
  int salt_begin = 0;
  int salt_end = 0;
  int enc_passwd_begin = 0;
  int enc_passwd_end = 0;
  int c_count;
  int dollar_count;
  int colon_count;
  int i;

  while (fgets(passwd_line,SIZE,pass_file_ptr)) {
     found_it = 0;
    dollar_count = 0;
    colon_count = 0;
    for (c_count = 0; c_count < SIZE; c_count++) {
      if (passwd_line[c_count] == '$') {
        dollar_count++;
        if (dollar_count == 1) {
          salt_begin = c_count ;
        } else if (dollar_count == 3) {
          salt_end = c_count;
        }
      } else if (passwd_line[c_count] == ':') {
        colon_count++;
        if (colon_count == 1) {
          for (i = 0; i < c_count; i++) {
            user_name[i] = passwd_line[i];
          }
          user_name[i] = '\0';
          enc_passwd_begin = c_count + 1;
        } else if (colon_count == 2) {
          enc_passwd_end = c_count ;
          c_count = SIZE;
        }
      }
    }

    for (i = salt_begin; i <= salt_end; i++) {
      salt[i-salt_begin] = passwd_line[i];
    }
    salt[i-salt_begin] = '\0';

    for (i = enc_passwd_begin; i < enc_passwd_end; i++) {
      encrypted_passwd[i-enc_passwd_begin] = passwd_line[i];
    }
    encrypted_passwd[i-enc_passwd_begin+1] = '\0';

    if(verbose) {
      fprintf(stdout, "\tUsager: %s\n", user_name);
    }

    run_dict();
    if (!found_it) {
      run_exhaustif(exhaustif);
    }
  }
}

int main ( int argc, char **argv) {
  int i;

  if (argc == 1) {
    err_message();
    exit(0);
  }

  for ( i = 1; i< argc; i++) {
    if (argv[i][0] == '-') {
      if (!strcmp(argv[i], "-help")) {
        err_message();
        exit(0);
      } else if (!strcmp(argv[i], "-v")  
                 || !strcmp(argv[i],"-verbose")) {
        verbose = 1;
      } else if (!strcmp(argv[i], "-pw")) {
        i++;
        strcpy(pass_file,argv[i]);
      } else if (!strcmp(argv[i], "-dict")) { 
        i++;
        strcpy(dict_file,argv[i]);
	dict_present = 1;
      } else if (!strcmp(argv[i], "-xl")) { 
        i++;
	exhaustif = atoi(argv[i]);
	if (exhaustif >= SIZE) {
          exhaustif = SIZE - 1;
	}
      } else if (!strcmp(argv[i], "-xc")) {
        i++;
	strcpy(fichier_exhaustif,argv[i]);
	fichier_exhaustif_present = 1;
      } else {
        err_message();
        exit(1);
      }
    } else {
      err_message();
      exit(1);
    }
  }

  if (!open_files()) {
    exit(1);
  }

  decryption();

  exit(0);
}
